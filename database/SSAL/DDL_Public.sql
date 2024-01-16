DROP TABLE IF EXISTS public.tramite_acceso cascade;
CREATE TABLE IF NOT EXISTS public.tramite_acceso(
	TA_ID bigint , --'Identificador del tramite generado '
	fecha_creacion timestamp NOT null, -- Fecha de creación de la solicitud de tramite
	fecha_ini timestamp NOT null, -- Fecha y hora de inicio de permiso
	Fecha_fin timestamp NOT NULL, -- Fecha y hora fin de permiso
	L_ID varchar(45) NOT null, -- Identificador del loca al cual se hara el permiso
	U_ID varchar(45) not null, -- Identificador del usuario quien solicita el permiso
	U_ID_resp_local varchar(45) not null, -- Identificador del usuario resposable del local
	U_ID_autoriza varchar(45) not null, -- identificador del usuario quien autoriza el acceso al local
	observaciones varchar(250)-- Campo que solo es modificado por el usuario que puede autorizar el acceso
);
alter table public.tramite_acceso add constraint PK_tramite_acceso_TA_ID primary key (TA_ID);

DROP TABLE IF EXISTS public.equipo_herramienta;
CREATE TABLE IF NOT EXISTS public.equipo_herramienta(
	EH_ID bigint not null, --'Identificador Equipo Herramienta'
	Descipcion varchar(50) not null, 
	Observaciones varchar(250),-- Campo que solo es modificado por el usuario que puede autorizar el acceso
	TA_ID bigint not null --'Identificador del tramite generado '
);
alter table public.equipo_herramienta add constraint PK_equipo_herramienta_EH_ID primary key (EH_ID);
alter table public.equipo_herramienta add constraint FK_equipo_herramienta_TA_ID foreign key (TA_ID) references public.tramite_acceso(TA_ID);

DROP TABLE IF EXISTS public.transporte;
CREATE TABLE IF NOT EXISTS public.transporte(
	TRAN_ID bigint not null, --'Identificador Equipo Herramienta'
	marca varchar(50) not null, -- Marca
	modelo varchar(50) not null, --'Modelo, categoria del transporte '
	placas varchar(50) not null, --'placas'
	color varchar(50) not null, --'Color'
	observaciones varchar(250),-- Observaciones respecto al transorte
	TA_ID bigint not null --'Identificador del tramite generado '
);
alter table public.transporte add constraint PK_transporte_TRAN_ID primary key (TRAN_ID);
alter table public.transporte add constraint FK_transporte_TA_ID foreign key (TA_ID) references public.tramite_acceso(TA_ID);


DROP TABLE IF EXISTS public.personal_ingreso;
CREATE TABLE IF NOT EXISTS public.personal_ingreso(
	PI_ID bigint not null, --'Identificador Equipo Herramienta'
	nombre varchar(50) not null, -- Nombre completo
	appat varchar(50) not null, -- Apellido Paterno
	apmat varchar(50),  -- Apellido Materno
	observaciones varchar(250),-- Campo que solo es modificado por el usuario que puede autorizar el acceso
	TA_ID bigint not null --'Identificador del tramite generado'
);
alter table public.personal_ingreso add constraint PK_personal_ingreso_PI_ID primary key (PI_ID);
alter table public.personal_ingreso add constraint FK_personal_ingreso_TA_ID foreign key (TA_ID) references public.tramite_acceso(TA_ID);

DROP TABLE IF EXISTS public.actividad;
CREATE TABLE IF NOT EXISTS public.actividad(
	ACT_ID bigint not null, --'Identificador Equipo Herramienta'
	descripcion varchar(100), -- Descripcion del catalogo de actividades
	observaciones varchar(250),-- Descripción de la actividad (Otros) cuando no se encuentra en el catalogo
	TA_ID bigint not null --'Identificador del tramite generado'
);
alter table public.actividad add constraint PK_actividad_ACT_ID primary key (ACT_ID);
alter table public.actividad add constraint FK_actividad_TA_ID foreign key (TA_ID) references public.tramite_acceso(TA_ID);