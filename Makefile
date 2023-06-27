.DEFAULT_GOAL := default #what does this line do?
########################## PACKAGE ACTIONS #####################
reinstall_package:
  @pip unistall -y rahna || : # -y flag avoids asking for confirmation
	@pip install -e .

########################## TESTS #####################
