import clr

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication 
app = uiapp.Application 
uidoc = uiapp.ActiveUIDocument

def tolist(obj):
	if isinstance(obj, list): return UnwrapElement(obj)
	else: return [UnwrapElement(obj)]

crv = UnwrapElement(IN[0])
p_segments = tolist(IN[1]) #list of segment lengths at which to place points

cRef = crv.GeometryCurve.Reference

# Start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)

for ps in p_segments:
	ps_feet = UnitUtils.Convert(ps, DisplayUnitType.DUT_METERS, DisplayUnitType.DUT_DECIMAL_FEET)
	refPt = app.Create.NewPointOnEdge(cRef,PointLocationOnCurve(PointOnCurveMeasurementType.SegmentLength, ps_feet, PointOnCurveMeasureFrom.Beginning))
	pt = doc.FamilyCreate.NewReferencePoint(refPt)

# End Transaction
TransactionManager.Instance.TransactionTaskDone()

OUT = pt