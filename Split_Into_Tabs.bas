Sub SplitDataToWorksheets()
    Dim srcWorksheet As Worksheet
    Dim destWorksheet As Worksheet
    Dim lastRow As Long
    Dim colIndex As Long
    Dim uniqueValues As Collection
    Dim cellValue As Variant
    
    ' Define the source worksheet where the data resides
    Set srcWorksheet = ThisWorkbook.Worksheets("Sheet1") ' Replace "Sheet1" with the actual name of your source worksheet
    
    ' Define the column index for splitting the data
    colIndex = 1 ' Replace with the column index (A=1, B=2, C=3, etc.) based on which you want to split the data
    
    ' Initialize a collection to store unique values
    Set uniqueValues = New Collection
    
    ' Loop through each cell in the specified column and store unique values in the collection
    On Error Resume Next
    For Each cellValue In srcWorksheet.Range(srcWorksheet.Cells(2, colIndex), srcWorksheet.Cells(srcWorksheet.Rows.Count, colIndex).End(xlUp)).Value
        uniqueValues.Add cellValue, CStr(cellValue)
    Next cellValue
    On Error GoTo 0
    
    ' Loop through each unique value in the collection
    For Each cellValue In uniqueValues
        ' Create a new worksheet for the current unique value
        Set destWorksheet = ThisWorkbook.Worksheets.Add(After:=ThisWorkbook.Worksheets(ThisWorkbook.Worksheets.Count))
        
        ' Copy the header row from the source worksheet to the destination worksheet
        srcWorksheet.Rows(1).Copy Destination:=destWorksheet.Rows(1)
        
        ' Loop through each row in the source worksheet
        lastRow = srcWorksheet.Cells(srcWorksheet.Rows.Count, colIndex).End(xlUp).Row
        For i = 2 To lastRow
            ' Check if the value in the specified column matches the current unique value
            If srcWorksheet.Cells(i, colIndex).Value = cellValue Then
                ' Copy the entire row to the destination worksheet
                srcWorksheet.Rows(i).Copy Destination:=destWorksheet.Rows(destWorksheet.Cells(destWorksheet.Rows.Count, colIndex).End(xlUp).Row + 1)
            End If
        Next i
        
        ' Rename the destination worksheet with the current unique value
        destWorksheet.Name = CStr(cellValue)
    Next cellValue
    
    ' Activate the source worksheet
    srcWorksheet.Activate
    
    ' Display a message box when the splitting is complete
    MsgBox "Splitting data into separate worksheets is complete.", vbInformation
End Sub