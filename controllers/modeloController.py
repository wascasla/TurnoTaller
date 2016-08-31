#controlador obras sociales
#encabezado = {'descripcion': 'Descripcion'}
@auth.requires_login()
def administrar_modelo():
    grid = SQLFORM.grid(db.modelo,user_signature=False,csv=False)
    return dict(grid=grid)