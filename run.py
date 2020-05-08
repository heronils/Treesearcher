if __name__ == '__main__':
	import regex
	from multiprocessing import Pool
	from treesearcher import tasks, do_cleanup, do_set_root, \
	do_set_fileexts, do_search, make_fs_name, write_toc

	#[of]set up some global stuff:set up some global stuff
	import variables
	globs = {
		'root': None,
		'fileexts': set(),
		'vars': {
			var[2:]: getattr(variables, var)
			for var in dir(variables) if var .startswith('p_')
		},
		'variableregex': regex.compile(r'{{([^{}]+)}}'),
		'newlineregex': regex.compile(r'\n'),
	}
	#[cf]

	import searches
	for typ, task in tasks:
		if typ == 'cleanup': do_cleanup(globs, ask=task)
		elif typ == 'setroot': do_set_root(globs, task)
		elif typ == 'setfileexts': do_set_fileexts(globs, task)
		elif typ == 'search':

			#[of]:ensure that basics options are configured
			if not globs['root']:
				abort('please define a root directory using set_root()')
			
			if not globs['fileexts']:
				abort('please define some file extensions using set_fileexts()')
			#[cf]
			#[of]:run the searches using multiple python processes
			todo = []
			for searchtitle, searchpattern in task.items():
				searchtitle = make_fs_name(searchtitle)
				todo.append((globs, searchtitle, searchpattern))
			
			print('starting search (may take a while)')
			
			pool = Pool()
			pool.map(do_search, todo)
			pool.close()
			pool.join()
			
			print('done')
			#[cf]

	write_toc(todo)

	print('ALL DONE')

