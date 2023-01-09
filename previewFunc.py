def previewFunc(delay=500, count=0):
    # the user input
    global searchEntry
    global lastQuery

    # the current mode [auto, filter, ...]
    global segemented_button_var
    global lastMode

    # what is currently shown at the screen
    global currentShowVar

    # the currently drawn (or at least was drawn) table
    global currentTableName
    # the CURRENTLY drawn column names which dont have to be the one in TMP
    global currentColumnNames

    # the preview mode toggle
    global checkbox
    global lastCheckBoxMode
    # shows also if preview mode is activated
    global showActivated

    # if the currentTableName swiched or was reclicked
    global justSwitchedTable

    userQuery = searchEntry.get().strip()
    mode = segemented_button_var.get()
    previewMode = checkbox.get()
    lastPreviewMode = lastCheckBoxMode

    def runAQueryOrNot(query):
        if query == "":
          # maybe the query is now empty but maybe wasnt before
          # so reset the UI to TMP
          updateUI(tmp)
          return

        previewTmp = tmp.editData(userQuery, mode, False)
        if previewTmp is None:
          # the user input is invalid
          # show the current state then
          updateUI(tmp)
        else:
          # the user input is valid, show the preview
          updateUI(previewTmp)

    # possible reasons the code has to be callen:
    # - preview mode was toggled
    # - user changed the query
    # - user changed the mode
    # - user switched to another table (or the same one)

    if not previewMode:
      # the preview mode is disabled

      # - the switching from one mode to another does not matter to a disabled preview
      # - the switching from one table to another does not matter to a disabled preview

      justSwitchedTable = False # we finished the complete switch by not applying the query since we dont want that

      # save performance by just reset the UI after a toggle
      if lastPreviewMode != previewMode:
        # the preview mode was toggled
        updateUI(tmp) # reset UI back to normal


      if userQuery == "":
        # if the user has no query (and the preview mode is off) then activate the buttons (like bin and add button)
        pageSystem.setTableState(customtkinter.NORMAL)
      else:
        # the preview mode is not active
        # but the user has written something so disable the UI
        pageSystem.setTableState(customtkinter.DISABLED)

    elif previewMode:
      # the preview mode is enabled

      # if the preview mode is enabled
      # NEVER allow any buttons like trash and add
      pageSystem.setTableState(customtkinter.DISABLED)

      # check if preview mode was toggled
      if lastPreviewMode != previewMode:
        # the preview mode was toggled

        # save the UI to tmp because of
        # bin button, add button etc
        tmp.setData(castColumns(currentTableName, currentColumnNames, pageSystem.getInput().copy()), currentColumnNames)
        updateUI(tmp) # TODO maybe not

        # since the query itself has not changed but we are now in active mode, we need to rerun the query and update the UI accordingly
        runAQueryOrNot(userQuery)

      # check if the query has changed
      if lastQuery != userQuery:
        # the user query has changed
        runAQueryOrNot(userQuery)

      if lastMode != mode:
        # the mode has changed, so rerun the query
        runAQueryOrNot(userQuery)

      if justSwitchedTable:
        # the user switched to another table
        runAQueryOrNot(userQuery)
        justSwitchedTable = False # we finished the complete switch by just applying the query

    lastCheckBoxMode = previewMode
    lastQuery = userQuery
    lastMode = mode

    tk.after(delay, lambda: previewFunc(delay, count + 1))