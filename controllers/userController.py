@auth.requires_membership('admin')
def administrar_user():	
    grid = SQLFORM.grid(db.auth_user,user_signature=False,csv=False)
    return dict(grid=grid)

@auth.requires_membership('admin')
def administrar_permisos():	
    grid = SQLFORM.grid(db.auth_membership,user_signature=False,csv=False)
    return dict(grid=grid)   