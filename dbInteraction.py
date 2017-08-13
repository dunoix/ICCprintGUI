from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def import CP, Compnd, Block



class sqlDB():
	# class vars
	

	def __init__(self):
		self.engineName = 'sqlite:///iccPrint.db'
		self.engine = create_engine(self.engineName)
		self.Session = sessionmaker(bind=self.engine)
		self.session = self.Session()

	#------------------------------------------	
	# Searches only one block
	def searchByBlock(self, bname):    
		qry = self.session.query(Block)
		bData = qry.filter(Block.bname == bname).first()
		qry = self.session.query(Compnd)
		cData = qry.filter(Compnd.id == bData.compnd_id).first()
		qry = self.session.query(CP)
		cpData = qry.filter(CP.id == cData.cp_id).first()
		
        
		return [[cpData.name, cData.cname, bData.bname, bData.btype]]

