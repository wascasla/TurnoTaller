# coding: utf8

db.define_table('obraSocial',
                Field('descripcion','string'),
                format='%(descripcion)s')

db.obraSocial.descripcion.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'obraSocial.descripcion')]

db.define_table('paciente',
    Field('nombres','string',
                      label='Nombres',
                      length=15),
    Field('apellidos','string',
                      label='Apellidos',
                      length=15),
    Field('dni','integer'),
    Field('fechaNac',
                      'date'),
    Field('obraSocial',db.obraSocial),
    Field('domicilio','string',
                      label='Domicilio',
                      length=50),
    Field('telFijo','integer',label='Tel Fijo',length=40),
    Field('celular','integer',label='Celular',length=40),
    Field('email','string',
                      label='Email',
                      length=40),   
    Field('created_by',db.auth_user,default=auth.user_id),
    Field('created_on','datetime',default=request.now,writable=False,readable=False),
    format='%(nombres)s, %(apellidos)s'
    )

db.paciente.dni.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'paciente.dni')]

#db.define_table('duration',
#    Field('description','text',label='Descripcion'),
#    Field('valor','integer'),
#    format='%(description)s')

db.define_table('task',
    Field('title','string'),
#    Field('task_type'),
    Field('paciente',db.paciente),
    Field('duracion','integer',label='Duracion (minutos)'),
    Field('description','text',label='Observacion'),
    Field('start_time','datetime',label='Fecha y Hora'),
    Field('stop_time','datetime',label='Fecha y Hora Fin'),
    Field('nro_sesion','integer',default=1),
    Field('concluido','boolean',default=False),
    Field('created_by',db.auth_user,default=auth.user_id,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False)
    )

#db.task.title.requires=IS_NOT_EMPTY()
#db.task.task_type.requires=IS_IN_SET(TASK_TYPES)
db.task.paciente.requires=IS_IN_DB(db,'paciente.id','%(nombres)s')
db.task.start_time.default=request.now
db.task.stop_time.default=db.task.start_time
#db.task.stop_time.default=request.now


#db.paciente.name.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'paciente.name')]
#db.paciente.company.requires=IS_IN_DB(db,'obraSocial.id','%(descripcion)s')
#db.paciente.phone.requires=is_phone
#db.paciente.fax.requires=is_phone

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
