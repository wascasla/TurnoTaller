#controlador obras sociales
#encabezado = {'descripcion': 'Descripcion'}
@auth.requires_login()
def administrar_marca():
    grid = SQLFORM.grid(db.marca,user_signature=False,csv=False)
    return dict(grid=grid)