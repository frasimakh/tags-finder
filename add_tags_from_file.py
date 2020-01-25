import click

from app import TAGS_MODEL

@click.command()
@click.argument('file_with_tags', type=click.Path(exists=True))
def main(file_with_tags):
    with open(file_with_tags) as tags_file:
        for line in tags_file:
            TAGS_MODEL.insert_tag(line.strip())


if __name__ == "__main__":
    main()
