#!/usr/bin/env python3

import random
import sys

from datetime import datetime
from pathlib import Path

import praw

import src.utils

SUBS_TO_CHECK = ['all']
RATE_OF_PERSISTENCE_OF_NEGATIVE_EXAMPLES = 10000  # 1-in-this-many non-xkcd-linking comments saved


def main():
	with open('creds', 'r') as f:
		creds = {k: v for k, v in [line.split('=') for line in f.read().splitlines()]}

	reddit = praw.Reddit(**creds, user_agent='xkcdBot')
	_ensure_data_structure_exists()
	global positives_file
	positives_file = Path('data', 'positive', str(datetime.now()).replace(' ', '_'))
	global negatives_file
	negatives_file = Path('data', 'negative', str(datetime.now()).replace(' ', '_'))
	
	positive_comments_persisted, negative_comments_persisted = 0, 0

	comments = reddit.subreddit('+'.join(SUBS_TO_CHECK)).stream.comments()
	for idx, comment in enumerate(comments):
		xkcd_link = src.utils.xkcd_linked_in_comment(comment)
		if xkcd_link is None:
			if not random.randint(0, RATE_OF_PERSISTENCE_OF_NEGATIVE_EXAMPLES):
				_persist_negative_example(comment, negative_comments_persisted)
				negative_comments_persisted += 1
		else:
			print(f'Persisting positive comments! comment is {comment.subreddit}/comments/{comment.submission.id}/foo/{comment.id}, and link is {xkcd_link}')
			_persist_positive_example(comment, xkcd_link, positive_comments_persisted)
			positive_comments_persisted += 1

		if not idx % 100 and idx != 0:
			print(f'{datetime.now()}: Handled {idx} comments!')


def _ensure_data_structure_exists():
	data_path = Path('data')
	if not data_path.exists():
		data_path.mkdir()

	positive_path = data_path.joinpath('positive')
	if not positive_path.exists():
		positive_path.mkdir()

	negative_path = data_path.joinpath('negative')
	if not negative_path.exists():
		negative_path.mkdir()


def _persist_positive_example(comment, link, num_persisted):
	# If I were a _real_ developer, I'd extract this (and below) to a class that would maintain
	# file-state.
	parent = comment.parent()
	if type(parent) == praw.models.reddit.submission.Submission:
		return

	global positives_file
	with positives_file.open('a') as f: # Grr - https://bugs.python.org/issue20218
		f.write_text(f'{link},{parent.id},{comment.submission.id},{parent.subreddit},{parent.body}\n')
	if not num_persisted % 1000:
		positives_file = Path('data', 'positive', str(datetime.now()).replace(' ', '_'))


def _persist_negative_example(comment, num_persisted):
	parent = comment.parent()
	if type(parent) == praw.models.reddit.submission.Submission:
		return

	global negatives_file
	with negatives_file.open('a') as f:
		f.write(f'{parent.id},{comment.submission.id},{parent.subreddit},{parent.body}\n')
	if not num_persisted % 1000:
		negatives_file = Path('data', 'negative', str(datetime.now()).replace(' ', '_'))


if __name__ == '__main__':
	sys.exit(main())