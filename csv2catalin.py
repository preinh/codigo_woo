import numpy as np
import fortranformat as ff

from hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser


_CATALOGUE = 'hmtk_bsb2013_pp_decluster.csv'
_CATALIN = 'catalin.d'

parser = CsvCatalogueParser(_CATALOGUE)
catalogue = parser.read_file()

catalogue.sort_catalogue_chronologically()

catalin_header_writer = ff.FortranRecordWriter('(28X,I6,/)')
output = catalin_header_writer.write([catalogue.get_number_events()]) + "\n"

catalin_line_writer = ff.FortranRecordWriter('(I5,I5,I5,I5,F7.3,7X,F7.3,46X,F3.1)')
for i in np.arange(0, catalogue.get_number_events(),1):
    yea = catalogue.data['year'][i]
    mon = catalogue.data['month'][i]
    day = catalogue.data['day'][i]
    dep = int(catalogue.data['depth'][i])
    x = float("%.4f"%catalogue.data['longitude'][i])
    y = float("%.4f"%catalogue.data['latitude'][i])
    mag = round(catalogue.data['magnitude'][i] ,1)
    line = [yea,mon,day,dep,x,y,mag]
    print line
    output += catalin_line_writer.write(line) + "\n"
    

f = open(_CATALIN, 'w')
f.write(output)
f.close()
