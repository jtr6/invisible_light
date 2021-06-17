import numpy as np
from astropy.io import fits 
from astropy.table import Table


def read_fits(filename):
    data = fits.open(filename)
    hdr = data[1].header
    table = data[1].data
    return table, hdr

def read_table(filename):
    return Table.read(filename)

def row_is_valid(row, lim):
    return (row["u_flux"] > lim) & (row["g_flux"] > lim) & (row["z_flux"] > lim) & (row["r_flux"] > lim) & (row["z_flux"] > lim) &\
        (row["J_flux"] > lim) & ((row["ch1_swire_flux"] > lim) or (row["ch1_servs_flux"] > lim)) & (row["F_SPIRE_250"] > lim) & \
        (row["F_PACS_160"] > lim) & (row["F_PACS_100"] > lim) & (row["K_flux"] > lim) & (row["F_MIPS_24"] > lim)


# 'u_flux','g_flux','r_flux','i_rcs_flux','z_flux','J_flux','K_flux', 'ch1_swire_flux', 'ch2_swire_flux',\
#           'ch3_swire_flux','ch4_swire_flux','F_MIPS_24','F_PACS_100','F_PACS_160', 'F_SPIRE_250','F_SPIRE_350',\
#           'F_SPIRE_500'

def short_table(table, lim):
    selection = Table(names = table.columns.names, dtype=table.columns.dtype)
    for row in table:
        if len(selection) >= 50:
            break
        elif row_is_valid(row, lim):
            selection.add_row(row)
    return(selection)


table, hdr = read_fits("lockman_optIR_catalogue_science_ready_photoz.fits")

lim = 10

new_table = short_table(table, lim)

primaryHDU = fits.PrimaryHDU()
tableHDU = fits.BinTableHDU(new_table, header=hdr)

hdul = fits.HDUList([primaryHDU, tableHDU])
hdul.writeto("LOFAR_galaxies.fits")