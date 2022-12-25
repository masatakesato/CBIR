from Preview import Plt_Preview
import pathlib


npz_path = pathlib.Path( "../data/wrangled/wrangled_000000.npz" )# './test_out.npz' )


if __name__=='__main__':
    Plt_Preview( npz_path, '3' )#'arr_0' )