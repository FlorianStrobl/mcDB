def einpflegen(tableBody):
  for row in range(numberRows):
            rowWidgets = []
            if tableBody[row] is None:
                continue
            for col in range(numberColumns + 1):
                if col < numberColumns:
                    myEntry = customtkinter.CTkEntry(
                        self.scrollFrame.viewPort,
                        corner_radius=0,
                        width=(widthCurrentFrame - self.actionColumnWidth)
                        / numberColumns,
                        fg_color=self.colors[self.colorIndex % 2],
                    )
                    myEntry.grid(row=row, column=col)

                    rowWidgets.append(myEntry)
                    try:
                        myEntry.insert(
                            0,
                            tableBody[row][col]
                            if tableBody[row][col] is not None
                            else "null",
                        )
                    except:
                        myEntry.insert(0, "Data not found")
                else:
                    deleteButton = customtkinter.CTkButton(
                        self.scrollFrame.viewPort,
                        text="🗑",
                        command=lambda row=row: self.onRemove(row),
                        corner_radius=0,
                        width=self.actionColumnWidth,
                        fg_color=self.colors[self.colorIndex % 2],
                    )
                    deleteButton["state"] = customtkinter.DISABLED
                    deleteButton.grid(row=row, column=col)
                    rowWidgets.append(deleteButton)