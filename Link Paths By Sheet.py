import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)
# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import *
# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
  
viewlist = UnwrapElement(IN[0]) #nested by sheet

for sheet in viewlist:
	sheetpaths=[]
	for view in sheet:
		#collect elements in view
		collector = Autodesk.Revit.DB.FilteredElementCollector(doc, view.Id) 
		
		viewpaths= []
		#collect DWG importinstances
		cadLinks = collector.OfClass(Autodesk.Revit.DB.ImportInstance)
		for cadlink in cadLinks:
			cadLinkType = doc.GetElement(cadlink.GetTypeId())
			viewpaths.append(ModelPathUtils.ConvertModelPathToUserVisiblePath(cadLinkType.GetExternalFileReference().GetAbsolutePath()))
			
		#collect RVT importinstances
		rtvLinks = collector.OfClass(Autodesk.Revit.DB.RevitImportInstance)
		for rvtlink in rvtLinks:
			rvtLinkType = doc.GetElement(rvtlink.GetTypeId())
			viewpaths.append(ModelPathUtils.ConvertModelPathToUserVisiblePath(rvtLinkType.GetExternalFileReference().GetAbsolutePath()))
	sheetpaths.append(viewpaths)

OUT = sheetpaths