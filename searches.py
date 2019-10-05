from treesearcher import *
import regex  # only needed if you define flags

#~ cleanup(ask=True)
set_root('C:/TiddlyWiki/TiddlyWiki5')
set_fileexts('+.tid')

search({
	#[of]:All tiddlers
	#[c]'None' lists all files
	#[c]
	#[c]

	'All tiddlers' : None,
	#[cf]
	#[of]:HTML linebreaks
	#[c]Some of these may be removed.
	#[c]
	#[c]

	'HTML linebreaks' : r'''

		#~ (?<=\n\s*)
		<br>
		#~ (*SKIP)
		#~ (?:
			#~ \s*
			#~ <br>(*SKIP)
		#~ )*
		#~ (?=\s*?\n)

	''',
	#[cf]
})

#[l]:Results:_toc.txt

if __name__ == '__main__':
	print('Nope, the run.py does the job')
