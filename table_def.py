# table_def.py
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///iccPrint.db')
Base = declarative_base()

########################################################################
class CP(Base):
    """"""
    __tablename__ = "cps"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, name):
        """"""
        self.name = name

#########################################################################
class Compnd(Base):
    __tablename__ = "compnd"

    id = Column(Integer, primary_key = True)
    cname = Column(String)

    cp_id = Column(Integer, ForeignKey("cps.id"))
    cp = relationship("CP", backref=backref("compnds", order_by=id))

    #-------------------------------------------------------------------
    def __init__(self, cname):
        self.cname = cname


########################################################################
class Block(Base):
    """"""
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True)
    bname = Column(String)
    btype = Column(String)
    bdata = Column(PickleType)

    compnd_id = Column(Integer, ForeignKey("compnd.id"))
    compnd = relationship("Compnd", backref=backref("blocks", order_by=id))


    #----------------------------------------------------------------------
    def __init__(self, bname, btype, bdata):
        """"""

        self.bname = bname
        self.btype = btype
        self.bdata = bdata


########################################################################

# create tables
Base.metadata.create_all(engine)



