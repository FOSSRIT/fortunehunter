from sugar.datastore import datastore
import os
import re
class BadInputException(Exception):pass

FILE_MIME = "application/x-fortune-map"
FM_VERSION = '1' #Must be string for dict


def export_textfile(activity, filename, dungeon_id, filetext=''):
    """
    Exports text to journal (in fortune map format)
    Requires activity instance, file name, dungeon id, and text

    @Returns: a DSObject representing the file in the datastore.
    """
    ds_objects, num_objects = datastore.find({'title':filename,'FortuneMaker_VERSION':FM_VERSION})

    if num_objects == 0:
        # Create a datastore object
        file_dsobject = datastore.create()

    else:
        file_dsobject = ds_objects[0]

    # Store unique id for easy search of journal
    file_dsobject.metadata['FM_UID'] = dungeon_id

    # Write any metadata (here we specifically set the title of the file and
    # specify that this is a plain text file).
    file_dsobject.metadata['title'] = filename
    file_dsobject.metadata['mime_type'] = FILE_MIME
    file_dsobject.metadata['FortuneMaker_VERSION'] = FM_VERSION

    #Write the actual file to the data directory of this activity's root.
    file_path = os.path.join(activity.get_activity_root(), 'instance', filename)
    f = open(file_path, 'w')
    try:
        f.write(filetext)
    finally:
        f.close()

    #Set the file_path in the datastore.
    file_dsobject.set_file_path(file_path)

    datastore.write(file_dsobject)
    file_dsobject.destroy()


def list_fh_files():
    ds_objects, num_objects = datastore.find({'FortuneMaker_VERSION':FM_VERSION})
    file_list = []
    for i in xrange(0, num_objects, 1):
        if ds_objects[i].metadata.has_key('FM_UID'):
            file_list.append( ds_objects[i] )
        else:
            #TODO: Attempt to read uid from file?
            pass
    return file_list

def load_dungeon_by_id(id):
    ds_objects, num_objects = datastore.find({'FortuneMaker_VERSION':FM_VERSION,'FM_UID':id})

    if num_objects == 0:
        return False

    return load_dungeon(ds_objects[0])

def load_dungeon(file_data):
    """
    Gets dungeon data dictionary from journal file object

    Internally opens file from xo journal object and calls do_load

    Throws BadInputException if failed to parse parts of the file
    """
    dgnFile=open(file_data.get_file_path(),'r')
    dungeon_data = do_load( dgnFile )
    dngFile.close()

    return dungeon_data

def do_load( dgnFile ):
    """
    Gets dungeon data dictionary from file stream

    Throws BadInputException if failed to parse parts of the file
    """
    grab = 0
    room_str = []
    for line in dgnFile:
        if grab == 0:
            name = line.strip()
            grab = 1

        elif grab == 1:
            d_id = line.strip()
            grab = 2

        elif grab == 2:
            match = re.match('(\d+)x(\d+)',line)
            if match:
                x = int(match.group(1))
                y = int(match.group(2))
                grab = 3
            else:
                raise BadInputException()

        elif grab == 3:
            theme = int(line)
            grab = 4

        elif grab == 4:
            next = line.strip()
            grab = 5

        elif grab == 5:
            room_str.append(line.strip())

    if grab == 5:
        dungeon_dict = {
            'name': name, 'theme': theme, 'next': next,
            'x': x, 'y': y, 'roomstr': room_str, 'd_id': d_id
        }
        return dungeon_dict

    else:
        raise BadInputException()
