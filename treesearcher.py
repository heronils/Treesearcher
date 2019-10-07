import os
import regex

#( API used in the searches.py
tasks = []
#[of]:cleanup
def cleanup(ask=True):
	tasks.append(('cleanup', ask))
#[cf]
#[of]:set root
def set_root(root):
	tasks.append(('setroot', root))

#[cf]
#[of]:set fileexts
def set_fileexts(*fileexts):
	tasks.append(('setfileexts', fileexts))

#[cf]
#[of]:search
def search(searches):
	tasks.append(('search', searches))
#[cf]
__all__ = 'cleanup set_root set_fileexts search' .split()
#)

#( API used in the run.py
#[of]:tools
def prnt(message):
	print(message, end='', flush=True)

def reading(filepath, encoding='utf-8'):
	return open(filepath, 'r', encoding=encoding)

def writing(filepath, encoding='utf-8'):
	return open(filepath, 'w', encoding=encoding)

def filecontents(filepath, encoding='utf-8'):
	try:
		with open(filepath, 'r', encoding=encoding) as f:
			return f .read()
	except UnicodeDecodeError as e:
		abort(
			"Could not read file with encoding 'utf-8':\n" +
			f"{filepath}\n" +
			'{e.args[0]}\n'
			'Sorry, i expect you to use utf-8 (no BOM) :-)\n'
			"Try Notepad++ -> 'Encoding' -> 'convert to utf-8'."
		)

def abort(message):
	print(message)
	print('ABORT')
	import sys; sys.exit(1)
#[cf]
#[of]:do cleanup
def do_cleanup(globs, ask=True):
	'''
	remove all files ending with '.txt' from the script directory
	'''

	#[of]:remove the files
	def remove_them(files_to_remove):
		prnt('Cleaning up result files ')
		for _, filepath in files_to_remove:
			os.remove(filepath)
			prnt('.')
		print(' done')
	#[cf]
	#[of]:collect the files to remove
	files_to_remove = []
	here = os.path.dirname(__file__)
	for filename in os.listdir(here):
		filepath = os.path.join(here, filename)
		if os.path.isfile(filepath) and filename .endswith('.txt'):
			files_to_remove .append((filename, filepath))
	#[cf]

	if files_to_remove:
		if ask:
			print('will remove the following files:')
			for filename, _ in files_to_remove:
				print(filename)
			yes = input("press 'y' to proceed\n")
			if yes:
				remove_them(files_to_remove)
			else:
				print('OK. Keeping these files')
		else:
			remove_them(files_to_remove)
	else:
		print(
			'no cleanup will be done, because there are no '
			'text files in this directory.'
		)
#[cf]
#[of]:do set root
def do_set_root(globs, root):
	'''
	Set the root directory where to search. Will visit child directories.
	'''
	root = os.path.abspath(os.path.normpath(root))
	if not os.path.exists(root):
		abort(f'Root directory does not exist:\n{root}')
	elif root != globs['root']:
		globs['root'] = root
		print(f'Root: {root}')
#[cf]
#[of]:do set fileexts
#[c]Todo: extend this (inlude/exclude dirs, regular expression patterns etc.)
#[c]

def do_set_fileexts(globs, exts):
	fileexts = globs['fileexts']
	for ext in exts:

		#[of]:parse ext and mode
		ext = ext .strip() .lower()
		if ext .startswith('-'):
			mode = 'remove'
			ext = ext .lstrip('-')
		else:
			mode = 'add'
			ext = ext .lstrip('+')
		if not ext .startswith(os.path.extsep):
			ext = os.path.extsep + ext
		#[cf]

		if mode == 'add':
			fileexts .add(ext)
		else:
			fileexts .remove(ext)
	if fileexts:
		prettyexts = '*' + ', *' .join(sorted(fileexts))
		print(f'File extensions: {prettyexts}')
	else:
		print('No file extensions defined')
#[cf]
#[of]do run:do search
def do_search(args):
	globs, searchtitle, searchpat = args
	print(f'  start : {searchtitle}')

	#[of]compile the runpattern:compile the searchpattern
	if searchpat:
		if not isinstance(searchpat, str):
			searchpat, flags = searchpat
			flags = flags|regex.VERBOSE
		else:
			flags = regex.VERBOSE

		#[of]substitute pattern variables in the runpattern:substitute pattern variables in the searchpattern
		#[c]Replace {{variable}} with the actual pattern
		#[c]defined in variables.py.
		#[c]

#[l]:variables.py:variables.py

		def handler(match):
			nonlocal globs
			var = ('_' .join(match[1] .split()) .lower())
			try:
				return globs['vars'][var]
			except KeyError:
				abort(f"could not find a definition for the variable '{var}'")

		while True:
			substituted = globs['var_pat'] .sub(handler, searchpat)
			if substituted == searchpat:
				break
			searchpat = substituted

		#[cf]

		try:
			searchpat = regex.compile(
				f'({searchpat})|(\\n)',
				flags
			)
		except regex.error as e:
			abort(f'Error compiling the searchpattern: {e.args[0]}')

	else:
		searchpat = None
	#[cf]
	#[of]write_runfile(runtitle, runpattern):search through the root dir and write results to the resultfile
	#[of]walklocs(root, runpattern):walk locations
	#[of]walk_ok_files(root):walk ok files
	def walk_ok_files(globs):
		fileexts = globs['fileexts']
		for dir, _, files in os.walk(globs['root']):
			for file in files:
				if os.path.splitext(file)[1] in fileexts:
					yield dir, file
	#[cf]

	def walk_locations(globs, searchpat):
		newline_pat = globs['newline_pat']

		for dir, file in walk_ok_files(globs):
			if searchpat is None:
				yield dir, file, 1
			else:

				#[of]:yield locations found in this file
				#[c]A location is the linenumber of a successful match.
				#[c]

				text = filecontents(os.path.join(dir, file))
				if text:
					loc = 1
					for match in searchpat .finditer(text):
						matched_text, newline = match[1], match[2]
						if newline:
							loc += 1
						elif matched_text:
							for _ in newline_pat .finditer(matched_text):
								loc += 1
							yield dir, file, loc
				#[cf]
	#[cf]
	#[of]escape_cb():escape cb
	def escape_cb(string):
		'''
		Escape strings which need to be escaped in titles of Code Browser
		sections and links
		'''
		return (string
			.replace('\\', '/')
			.replace(':', '\\:')
		)
	#[cf]
	#[of]section_opener(title):section opener
	def section_opener(title):
		''' opens a Code Browser section '''
		return f'#[of]:{escape_cb(title)}\n'
	#[cf]
	section_closer = '#[cf]\n'
	#[of]link(dir, file, loc):filelink
	def filelink(dir, file, loc):
		''' create a Code Browser link to a line in a file '''
		dir = escape_cb(dir)
		file = escape_cb(file)
		target = f'file\:///{dir}/{file}?aln={loc}'
		return f'#[l]:{file}:{target}\n'
	#[cf]

	root = globs['root']
	with writing(searchtitle + '.txt') as f:
		curdir = None
		for dir, file, loc in walk_locations(globs, searchpat):
			if curdir != dir:
				if curdir:
					f .write(section_closer)
				f .write(section_opener(os.path.relpath(dir, root)))
				curdir = dir
			f .write(filelink(curdir, file, loc))
		if curdir:
			f .write(section_closer)
		else:
			f .write('Nothing found')
	#[cf]

	print(f'  done  : {searchtitle}')
#[cf]
#[of]make_fs_name(runtitle):make fs name
#[of]Invalid things in (mostly Windows) filenames:Invalid things in (mostly Windows) filenames
#[c]https://stackoverflow.com/a/31976060/1658543
#[c]

invalid_chars = regex.compile(r'[<>:"/\\|?*]')
invalid_end = regex.compile(r'[\s.]*$')
invalid_filenames = set('''
	CON PRN AUX NUL
	COM1 COM2 COM3 COM4 COM5 COM6 COM7 COM8 COM9
	LPT1 LPT2 LPT3 LPT4 LPT5 LPT6 LPT7 LPT8 LPT9
	_toc
''' .split())

searchcounter = 0
#[cf]

def make_fs_name(searchtitle):
	global searchcounter
	searchcounter += 1
	t = searchtitle
	t = invalid_chars .sub('_', t)
	t = invalid_end .sub('', t) .lstrip()
	while t .endswith('.txt'):
		t = t[:-4] .rstrip()
		t = invalid_end .sub('', t)
	t = ' ' .join(t .split())
	if not t:
		abort(
			f'Search number {searchcounter} has ' +
			'an empty title after normalisation'
		)
	if t in invalid_filenames:
		abort(
			f"The search title '{t}' is a reserved name"
		)
	return t
#[cf]
#[of]write_index(runtitles):write toc
#[of]link(runtitle):resultlink(searchtitle)
def resultlink(searchtitle):
	return f'#[l]:{searchtitle}:{searchtitle}.txt\n'
#[cf]

def write_toc(data):
	here = os.path.dirname(__file__)

	#[of]:old, new = collect new and old result files
	new = [searchtitle for _, searchtitle, _ in data]
	old = []

	for file in os.listdir(here):
		if os.path.isfile(file) \
		and file .endswith('.txt') \
		and file != '_toc.txt':
			file = file[:-4]
			if file not in new:
				old.append(file)
	#[cf]

	tocpath = os.path.join(here, '_toc.txt')
	prnt(f'Writing _toc.txt ... ')
	with open(tocpath, 'w', encoding='utf-8') as f:
		if not old and not new:
			f .write('Nothing found\n')
		else:
			if new:
				f .write('New:\n')
				for searchtitle in new:
					f .write(resultlink(searchtitle))
			if old and new:
				f .write('\n')
			if old:
				f .write('Old:\n')
				for searchtitle in sorted(old):
					f .write(resultlink(searchtitle))
	print('done')
#[cf]
#)

if __name__ == '__main__':
	print('Nope, the run.py does the job')
