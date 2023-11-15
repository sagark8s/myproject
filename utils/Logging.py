from inspect import currentframe, getframeinfo


debug = lambda message,frameinfo=getframeinfo(currentframe()):print(f"{frameinfo.filename},{frameinfo.lineno}:{message}")
