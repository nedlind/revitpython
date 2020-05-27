import clr

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import ReferencePointArray

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Unwrap 
refPts = UnwrapElement(IN[0])

# Start Transaction
doc = DocumentManager.Instance.CurrentDBDocument
TransactionManager.Instance.EnsureInTransaction(doc)

# Make the CurveByPoints
arr = ReferencePointArray()
for pt in refPts:
	arr.Append(pt)
cbp = doc.FamilyCreate.NewCurveByPoints(arr)

# End Transaction
TransactionManager.Instance.TransactionTaskDone()

# Wrap
OUT = cbp.ToDSType(0)