import os


def file_check(fname,dty=None) -> bool:
    """
    fname : the file name to be searched is
    ,dty : if None it searches in the directory it is in,
    if you want to search in another directory,
    type the path of that directory
    """
    if dty is None:
        location: list[str] = os.listdir()
    elif type(dty)==str:
        location = os.listdir(dty)

    for x in location:
        if x == fname:
            return True
    return False

def control_file_create(file_name,go_inside=True) -> None:
    """
    file_name: the name of the folder that should be checked in the directory you are in,
    or should be created and entered directly, if any
    """
    fc: bool = file_check(file_name)
    if not fc:
        os.mkdir(file_name)

    if go_inside:
        os.chdir(file_name)
    del fc
