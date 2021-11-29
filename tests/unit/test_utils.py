from Util import (
    create_directory,
)


def test_create_dictionary(tmp_path):
    create_directory(str(tmp_path)+'/test')
    assert len(list(tmp_path.iterdir())) == 1



