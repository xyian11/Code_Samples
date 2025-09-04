Sub ExportWorksheetsToUTF8TextFiles()
    Dim ws As Worksheet
    Dim folderPath As String
    Dim fileName As String
    Dim fileNumber As Integer
    
    ' Prompt the user to select a folder to save the text files
    folderPath = MacScript("return POSIX path of (choose folder with prompt ""Select a Folder"")")
    
    If folderPath = "" Then
        Exit Sub ' User canceled, exit the sub
    End If
    
    ' Loop through each worksheet in the workbook
    For Each ws In ThisWorkbook.Worksheets
        ' Generate the file name for the current worksheet
        fileName = folderPath & "/" & ws.Name & ".txt"
        
        ' Open the text file for output as UTF-8 encoded
        fileNumber = FreeFile
        Open fileName For Output As #fileNumber
        
        ' Loop through each row in the worksheet
        Dim lastRow As Long
        lastRow = ws.Cells(Rows.Count, 1).End(xlUp).row
        
        Dim row As Long
        
        For row = 1 To lastRow
            ' Check if the entire row is blank
            If WorksheetFunction.CountA(ws.Rows(row)) > 0 Then
                ' Loop through each column in the row and write the cell values to the text file
                Dim lastCol As Long
                lastCol = ws.Cells(row, Columns.Count).End(xlToLeft).Column
                
                Dim col As Long
                
                For col = 1 To lastCol
                    ' Write the cell value to the text file
                    Print #fileNumber, ws.Cells(row, col).Value;
                    
                    ' Add a tab delimiter after each cell except the last one in the row
                    If col < lastCol Then
                        Print #fileNumber, vbTab;
                    End If
                Next col
                
                ' Move to the next line after each row
                Print #fileNumber, ""
            End If
        Next row
        
        ' Close the text file
        Close #fileNumber
    Next ws
    
    ' Display a message box when the export is complete
    MsgBox "Export complete.", vbInformation
End Sub