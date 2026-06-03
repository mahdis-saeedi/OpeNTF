
import pickle
import pandas as pd
def generate_i2g_and_female_csv(c2g_file, c2i_file, output_dir):
    """
    Generate i2g mapping (col_index: (isfemale, acc)) and save csv with column indexes where isfemale==True.
    - c2g_file: pickle file for expert's idname -> gender (idname: (isfemale, acc)), ideally the superset and includes for all experts
    - c2i_file: pickle file for index.pkl in opentf that has (idname: index), ideally subset including the ones after some filterings
    """
    with open(c2g_file, 'rb') as f: c2g = pickle.load(f)
    with open(c2i_file, 'rb') as f: c2i = pickle.load(f)['c2i']

    i2g = {}; missing_ids = []
    for idname, col_idx in c2i.items():
        try: i2g[col_idx] = c2g[idname]
        except KeyError: missing_ids.append(idname)
    if len(missing_ids) > 0: print(f'The following {len(missing_ids)} idnames in c2i are missing in c2g: {missing_ids}')
    with open(f'{output_dir}i2g.pkl', 'wb') as f: pickle.dump(i2g, f)

    female_columns = sorted(idx for idx, (isfemale, acc) in i2g.items() if isfemale is True)
    pd.DataFrame(female_columns, columns=['teamsvecs-females-col-idx']).to_csv(f'{output_dir}females.csv', index=False)


if __name__ == "__main__":
    c2g_file = r"C:\Mahdis\c2g.pkl"
    c2i_file = r"C:\Mahdis\indexes.pkl"
    output_dir = r"C:\Mahdis\\"   # make sure it ends with /
    import os


    generate_i2g_and_female_csv(c2g_file, c2i_file, output_dir)