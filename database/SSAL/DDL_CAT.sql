-- DROP TABLE IF EXISTS cat.CatalogoRelCatalogo

-- DROP TABLE IF EXISTS cat.CatalogoDetalle

-- DROP TABLE IF EXISTS cat.Catalogo

CREATE TABLE IF NOT EXISTS cat.Catalogo (
  	CAT_ID varchar(15) NOT NULL,
	CAT_Descripcion varchar(50) NOT NULL,
	CAT_Administra varchar(50) NOT NULL,
	EF_ID varchar(4) NULL,
  CONSTRAINT CAT_PK PRIMARY KEY (CAT_ID)
) ;

CREATE TABLE IF NOT EXISTS cat.CatalogoDetalle (
  	CATD_ID varchar(50) NOT NULL,
	CATD_Descripcion varchar(100) NOT NULL,
	CATD_CVE_Oiriginal varchar(45) NOT NULL,
	CAT_ID varchar(15) NOT NULL,
	CATD_InfoAdicional json NULL,
  CONSTRAINT CATD_PK PRIMARY KEY (CATD_ID),
  CONSTRAINT CATD_CAT_FK FOREIGN KEY (CAT_ID) REFERENCES cat.Catalogo (CAT_ID)
);

CREATE TABLE IF NOT EXISTS cat.CatalogoRelCatalogo (
	CATD_ID_Padre varchar(50) NOT NULL,
	CATD_ID_Hijo varchar(50) NOT NULL,
	CATD_ID_TipoRelacion varchar(50) NOT NULL,
  CONSTRAINT CARE_PK PRIMARY KEY (CATD_ID_Hijo,CATD_ID_Padre),
  CONSTRAINT CRC_CATD_Hijo FOREIGN KEY (CATD_ID_Hijo) REFERENCES cat.CatalogoDetalle (CATD_ID),
  CONSTRAINT CRC_CATD_Padre FOREIGN KEY (CATD_ID_Padre) REFERENCES cat.CatalogoDetalle (CATD_ID),
  CONSTRAINT CRC_CATD_TipoRelacion FOREIGN KEY (CATD_ID_TipoRelacion) REFERENCES cat.CatalogoDetalle (CATD_ID)
) ;
