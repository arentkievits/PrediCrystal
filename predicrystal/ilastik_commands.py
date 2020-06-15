"This library is used to create the command line input for pixel classification and object classification"


MAX_LEN = 8191  # the maximum length of the string in command prompt (XP or later)


def chunks(l, n):
    """Yield n number of striped chunks from l."""
    for i in range(0, n):
        yield l[i::n]


def create_pixel_class_command(data_files: str, output_folder: str, project_file: str):
    # use a truncated path for the data in the headless operation mode of Ilastik to limit string length
    trunc_data_files = [p.relative_to(p.parents[1]) for p in data_files]
    trunc_data_files = [str(p) for p in trunc_data_files]  # convert to str
    
    output_filename_format = output_folder / '{nickname}_Prob.h5'

    for n in range(1, 10):
        raw_chunks = list(chunks(trunc_data_files, n))

        cmds = []

        for raw_chunk in raw_chunks:
            raw_chunk = list(raw_chunk)

            raw_data=' '.join(raw_chunk)  # tiff_files_from_mrc/mrc_00000.tiff ... 
            
            cmd = (
                f'run-ilastik.bat'
                f' --headless'
                f' --project={project_file}'
                f' --output_filename_format={output_filename_format}'
                f' --export_source="Probabilities"'
                f' --raw_data {raw_data}'
            )

            cmds.append(cmd)

        if all(len(s) < MAX_LEN for s in cmds):
            break

    return cmds


def create_object_class_command(data_files:str, pixel_files:str, output_folder:str, project_file:str):
    # use a truncated path for the data in the headless operation mode of Ilastik to limit string length
    trunc_data_files = [p.relative_to(p.parents[1]) for p in data_files]
    trunc_data_files = [str(p) for p in trunc_data_files]  # convert to str

    # used also a truncated path for the pixel classification data in the headless operation mode of Ilastik to limit string length
    trunc_path = [p.relative_to(p.parents[1]) for p in pixel_files]
    trunc_path = [str(p) for p in trunc_path]  # convert to str

    output_filename_format = output_folder / '{nickname}_{result_type}.h5'
    table_filename = output_folder / 'exported_data-{nickname}.csv'

    assert len(trunc_path) == len(trunc_data_files)

    for n in range(1, 10):
        raw_chunks = list(chunks(trunc_data_files, n))
        pixel_chunks = list(chunks(trunc_path, n))

        assert len(raw_chunks) == len(pixel_chunks)

        cmds = []

        for raw_chunk, pixel_chunk in zip(raw_chunks, pixel_chunks):
            raw_chunk = list(raw_chunk)
            pixel_chunk = list(pixel_chunk)
            assert len(raw_chunk) == len(pixel_chunk)

            raw_data=' '.join(raw_chunk)  # tiff_files_from_mrc/mrc_00000.tiff ... 
            prediction_maps=' '.join(pixel_chunk)  # ilastik_output_04-28_17-18-19/mrc_00000_Prob.h5 ... 
            
            cmd = (
                f'run-ilastik.bat'
                f' --headless'
                f' --project={project_file}'
                f' --output_filename_format={output_filename_format}'
                f' --table_filename={table_filename}'
                f' --export_source="Object Predictions"'
                f' --raw_data {raw_data}'
                f' --prediction_maps {prediction_maps}'
            )

            cmds.append(cmd)

        if all(len(s) < MAX_LEN for s in cmds):
            break

    return cmds

