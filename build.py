#!/usr/bin/env python3
# Baut die kommParl-Spezifikation aus den Quellen in src/, schema/ und examples/.
#
# Grundlage ist build.py aus OParl/spec (CC BY-SA 4.0). Für kommParl angepasst;
# die Änderungen stehen in HERKUNFT.md.

import os
import shlex
import shutil
import subprocess
import sys
from argparse import ArgumentParser
from glob import glob
from os import path

from scripts.json_schema2markdown import schema_to_markdown

SPECIFICATION_NAME = 'kommParl'

SPECIFICATION_BUILD_ACTIONS = [
    'all',
    'clean',
    'test',
    'live',
    'html',
    'pdf',
    'odt',
    'docx',
    'txt',
    'epub',
    'archives',
    'zip',
    'gz',
    'bz'
]

# Werkzeuge, die jede Ausgabe braucht (Text und Abbildungen)
SPECIFICATION_BUILD_TOOLS = [
    'pandoc',
    'dot',
    'gs',
    'convert'
]

# Werkzeuge, die nur einzelne Aktionen brauchen
SPECIFICATION_BUILD_TOOLS_BY_ACTION = {
    'pdf': ['xelatex'],
    'all': ['xelatex'],
    'zip': ['xelatex', 'zip'],
    'gz': ['xelatex', 'tar'],
    'bz': ['xelatex', 'tar'],
    'archives': ['xelatex', 'zip', 'tar']
}

SPECIFICATION_BUILD_FLAGS = {
    'gs': '-dQUIET -dSAFER -dBATCH -dNOPAUSE -sDisplayHandle=0 -sDEVICE=png16m -r600 -dTextAlphaBits=4',
    'pandoc': '--from markdown --standalone --table-of-contents --toc-depth=2 --number-sections'
}


def configure_argument_parser():
    parser = ArgumentParser(
        prog='./build.py',
        epilog='''
            build.py is part of the kommParl specification, which is based on
            the OParl specification, and is distributed under the terms of the
            Creative Commons Attribution-ShareAlike 4.0 License.
        '''
    )

    parser.add_argument(
        '--language',
        '-l',
        help='Specification language',
        default='de',
        action='store',
    )

    parser.add_argument(
        '--version',
        '-V',
        help='This will be displayed as version in the specification. Defaults to the draft state of the current commit',
        action='store',
    )

    parser.add_argument(
        '--print-basename',
        help='This will output the base name used for build output',
        action='store_true',
        dest='print_basename'
    )

    parser.add_argument(
        '--latex-template',
        help='Change the latex template used for PDF generation',
        action='store',
        default='resources/template.tex'
    )

    parser.add_argument(
        '--html-style',
        help='Change the CSS file used for styling the HTML output',
        action='store',
        default='resources/html5.css'
    )

    parser.add_argument(
        '--list-actions',
        help='List available build actions',
        dest='list_actions',
        action='store_true'
    )

    parser.add_argument(
        'action',
        help='Build action to take, available actions are: {}'.format(', '.join(SPECIFICATION_BUILD_ACTIONS)),
        action='store',
        nargs='*'
    )

    return parser


def check_build_action(action):
    if len(action) == 0:
        return 'all'

    if action[0] in SPECIFICATION_BUILD_ACTIONS:
        return action[0]

    raise Exception(
        'Unknown build action: {}, choose one of: {}'.format(action, ', '.join(SPECIFICATION_BUILD_ACTIONS)))


def get_default_version():
    """
    kommParl ist ein Entwurf ohne eigene Versionsnummer. Bis zur ersten
    Veröffentlichung kennzeichnet der Commit den Stand. Die Tags des Repositorys
    stammen aus dem Original und bezeichnen dessen Versionen; sie werden hier
    deshalb nicht ausgewertet.
    """
    try:
        commit = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'],
            universal_newlines=True,
            stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return 'entwurf'

    return 'entwurf-g{}'.format(commit)


def check_available_tools(action):
    tools = {}
    for tool in SPECIFICATION_BUILD_TOOLS + SPECIFICATION_BUILD_TOOLS_BY_ACTION.get(action, []):
        executable = shutil.which(tool)
        if not executable and tool == 'convert':
            # ImageMagick 7 nennt das Programm `magick`
            executable = shutil.which('magick')

        if executable:
            tools[tool] = executable
        else:
            raise Exception('{} not found, aborting.'.format(tool))

    return tools


def get_filename_base(language, version):
    return '{}-{}-{}'.format(SPECIFICATION_NAME, version, language)


def prepare_builddir(filename_base):
    os.makedirs('build/src/images')
    os.makedirs('build/{}'.format(filename_base))


def prepare_schema(language):
    language_file = 'schema/strings.yml'
    if language != 'de':
        language_file = 'locales/{}/schema/strings.yml'.format(language)

    output_file = 'build/src/3-99-schema.md'

    schema_to_markdown('schema', 'examples', output_file, language, language_file)


def prepare_markdown(language, version):
    glob_pattern = 'src/*.md'
    if language != 'de':
        glob_pattern = 'locales/{}/src/*.md'.format(language)

    files = glob(glob_pattern)
    for f in files:
        shutil.copy2(f, 'build/src/')

    os.mkdir('build/extra')
    with open('build/extra/detailed-version.md', 'w') as fp:
        fp.write("Version {}\n".format(version))


def prepare_images(tools):
    glob_pattern = 'src/images/*.*'

    files = glob(glob_pattern)
    for f in files:
        convert_command = ''
        filename, extension = os.path.splitext(f)
        fout = path.join('build', 'src', 'images', os.path.basename(filename) + '.png')

        shutil.copy2(f, fout)

        if extension == '.pdf':
            convert_command = '{} {} -sOutputFile={} -f {}'.format(
                tools['gs'],
                SPECIFICATION_BUILD_FLAGS['gs'],
                fout,
                f
            )

        if extension == '.dot':
            convert_command = '{} -Tpng {} -o {}'.format(
                tools['dot'],
                f,
                fout
            )

        if extension == '.svg':
            convert_command = '{} {} {}'.format(
                tools['convert'],
                f,
                fout
            )

        cmd = shlex.split(convert_command)
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            raise Exception(
                'Errored on image prep for {}, please check the command:\n{}'.format(
                    f, convert_command
                )
            )


def create_symlinks(filename_base):
    """ Allow having stable links when working on the spec """
    os.makedirs('build/latest')
    for specfile in os.listdir('build/{}'.format(filename_base)):
        existing = os.path.abspath('build/{}/{}'.format(filename_base, specfile))
        new = 'build/latest/{}{}'.format(SPECIFICATION_NAME.lower(), os.path.splitext(specfile)[-1])
        try:
            os.symlink(existing, new)
        except OSError:
            # Ohne Berechtigung für symbolische Verknüpfungen (z. B. unter Windows)
            shutil.copy2(existing, new)


def get_pandoc_version(pandoc_bin):
    version_tuple = subprocess.getoutput('{} --version'.format(pandoc_bin)).split('\n')[0].split(' ')[1].split('.')
    return [int(v) for v in version_tuple]


def run_pandoc(pandoc_bin, options, filename_base, output_format, extra_args='', extra_files=''):
    output_file = 'build/{}/{}.{}'.format(filename_base, filename_base, output_format)
    if path.exists(output_file):
        return

    source_files = glob('build/src/*.md')
    source_files.sort(key=lambda file: path.basename(file))
    # This gets the version into the titlepage of the pdf
    detailed_version = '-M detailed-version={}'.format(options.version)

    # NOTE: Once we can safely assume pandoc 2.0, we can use resource-path
    #       for neater include management in the markdown files
    # pandoc_command = '{} {} {} --resource-path=.:build/src -o {} {} {}'.format(
    pandoc_command = '{} {} {} -o {} {} {} {}'.format(
        pandoc_bin,
        SPECIFICATION_BUILD_FLAGS['pandoc'],
        extra_args,
        output_file,
        extra_files,
        detailed_version,
        ' '.join(source_files)
    )

    cmd = shlex.split(pandoc_command)
    try:
        subprocess.run(cmd, check=True, stdout=sys.stdout, stderr=sys.stderr)
    except subprocess.CalledProcessError:
        raise Exception(
            'Errored on pandoc: {}'.format(pandoc_command)
        )


class Action:
    @staticmethod
    def clean():
        shutil.rmtree('build', ignore_errors=True)

    @staticmethod
    def live(tools, options, filename_base):
        args = '--to html5 --section-divs --no-highlight --template=resources/live.html'
        run_pandoc(tools['pandoc'], options, filename_base, 'html', extra_args=args)

    @staticmethod
    def html(tools, options, filename_base):
        # pandoc 2.19 hat --self-contained durch --embed-resources ersetzt
        embed = '--self-contained'
        if get_pandoc_version(tools['pandoc'])[:2] >= [2, 19]:
            embed = '--embed-resources'

        args = '--to html5 --css {} --section-divs {}'.format(options.html_style, embed)
        run_pandoc(tools['pandoc'], options, filename_base, 'html', extra_args=args,
                   extra_files='build/extra/detailed-version.md resources/lizenz-als-bild.md')

    @staticmethod
    def pdf(tools, options, filename_base):
        args = '--pdf-engine=xelatex'
        if get_pandoc_version(tools['pandoc'])[0] < 2:
            args = '--latex-engine=xelatex'

        args += ' --template {}'.format(options.latex_template)

        run_pandoc(tools['pandoc'], options, filename_base, 'pdf', extra_args=args)

    @staticmethod
    def odt(tools, options, filename_base):
        run_pandoc(tools['pandoc'], options, filename_base, 'odt',
                   extra_files='build/extra/detailed-version.md resources/lizenz-als-text.md')

    @staticmethod
    def docx(tools, options, filename_base):
        run_pandoc(tools['pandoc'], options, filename_base, 'docx',
                   extra_files='build/extra/detailed-version.md resources/lizenz-als-text.md')

    @staticmethod
    def txt(tools, options, filename_base):
        run_pandoc(tools['pandoc'], options, filename_base, 'txt')

    @staticmethod
    def epub(tools, options, filename_base):
        run_pandoc(tools['pandoc'], options, filename_base, 'epub', extra_files='build/extra/detailed-version.md')

    @staticmethod
    def all(tools, options, filename_base):
        Action.html(tools, options, filename_base)
        Action.pdf(tools, options, filename_base)
        Action.odt(tools, options, filename_base)
        Action.docx(tools, options, filename_base)
        Action.txt(tools, options, filename_base)
        Action.epub(tools, options, filename_base)

    @staticmethod
    def zip(tools, options, filename_base):
        Action.all(tools, options, filename_base)
        archive_name = '{}.zip'.format(filename_base)
        subprocess.run(['zip', '-qr', archive_name, filename_base], cwd='build')

    @staticmethod
    def gz(tools, options, filename_base):
        Action.all(tools, options, filename_base)
        archive_name = '{}.tar.gz'.format(filename_base)
        subprocess.run(['tar', '-czf', archive_name, filename_base], cwd='build')

    @staticmethod
    def bz(tools, options, filename_base):
        Action.all(tools, options, filename_base)
        archive_name = '{}.tar.bz2'.format(filename_base)
        subprocess.run(['tar', '-cjf', archive_name, filename_base], cwd='build')

    @staticmethod
    def archives(tools, options, filename_base):
        Action.zip(tools, options, filename_base)
        Action.gz(tools, options, filename_base)
        Action.bz(tools, options, filename_base)


def main():
    options = configure_argument_parser().parse_args()
    action = check_build_action(options.action)

    if options.version is None:
        options.version = get_default_version()

    filename_base = get_filename_base(options.language, options.version)

    if options.print_basename:
        print(filename_base)
        exit(0)

    if options.list_actions:
        for action in SPECIFICATION_BUILD_ACTIONS:
            print('- ' + action)
        exit()

    if action == 'test':
        # Schemas und Beispiele prüfen, ohne etwas zu bauen
        from scripts.validate import main as validate
        exit(validate())

    # always clean
    Action.clean()

    if action == 'clean':
        exit(0)

    tools = check_available_tools(action)

    prepare_builddir(filename_base)
    prepare_schema(options.language)
    prepare_markdown(options.language, options.version)
    prepare_images(tools)

    # Avoid much boilerplate
    getattr(Action, action)(tools, options, filename_base)

    create_symlinks(filename_base)


if __name__ == '__main__':
    main()
