from treesearcher import *
import regex
#[of]Regex cheatsheet:Regex cheatsheet
#[c]\m 				'start of word'
#[c]\M				'end of word'
#[c](*PRUNE)
#[c](*SKIP)			'do not backtrack from this point on'
#[cf]

#[c]Inspect site-packages

set_root('C:/_/python37/Lib/site-packages')
set_fileexts('+.py')
#[c]~ cleanup(ask=False)

search({
	#[of]classes:code examples
	"code examples" : [
		r'''
		(?<!
			^  {{ inline ws }} {{ do not backtrack }}
			(?:
				>>> {{ something }}
				|
				{{ three dots }} {{ maybe something }}
			)  \n
		)
		^  {{ inline ws }}  >>>  {{ inline ws }} {{ do not backtrack }}  .
		''',
		regex.MULTILINE
	],
	#[cf]
	#[of]classes:~ all files
	#[c]~ "all files" : None,
	#[cf]
	#[of]classes:~ classes
	#[c]~ "classes" : [
	#[c]	~ r'{{ class keyword }}',
	#[c]	~ regex.MULTILINE
	#[c]~ ],
	#[cf]
	#[of]functions:~ functions
	#[c]~ "functions" : [
	#[c]	~ r'{{ function keyword }}',
	#[c]	~ regex.MULTILINE
	#[c]~ ],
	#[cf]
})

#[l]:run.py:run.py
#[l]:results:_toc.txt

if __name__ == '__main__':
	print('Nope, the run.py does the job')

#[of]:~ Old
#[c]( options

#[c]~ ~ cleanup(ask=False)

#[c]Set this to the root directory
#[c]~ set_root('C:/_/python37/Lib')

#[c]Search in python files
#[c]~ set_fileexts('+.py')

#[c]~ search({
#[c]	~ "'tw.boot.startup'" : r'''
#[c]		~ \$tw[.]boot[.]startup
#[c]	~ ''',
#[c]	~ ~ "'tw.boot.tasks'" : r'''
#[c]		~ ~ \$tw[.]boot[.]tasks
#[c]	~ ~ ''',
#[c]	~ ~ "'tw.boot.bootPath'" : r'''
#[c]		~ ~ \$tw[.]boot[.]bootPath
#[c]	~ ~ ''',
#[c]	~ ~ "'includeWikis'" : r'''
#[c]		~ ~ "includeWikis"
#[c]	~ ~ ''',
#[c]~ })

#[l]:run:run.py
#[l]:results:_toc.txt
#[cf]
