import os, shutil

#Change to current folder & remove current venv
os.chdir('.')
if os.path.isdir('venv'):
    shutil.rmtree('venv')

#Go through all the python files and get the list of pip commands
pip_commands = []
for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):            #Filter only Python files
            with open(os.path.join(root, file), 'r', errors='replace') as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip().startswith('#pip') or line.strip().startswith('# pip'):
                        pip_commands.append(line.replace('#','').strip())

print(pip_commands)

#Create batch file
os.system('python -m venv venv')
#batch += 'python -m venv venv\n'
batch = 'venv\\Scripts\\activate.bat &&'
batch += ' && '.join(pip_commands)
batch += ' && pip freeze > requirements.txt'

os.system(batch)
