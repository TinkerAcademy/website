function getCallerClass(a,b){for(var c=a.getStackTrace(),d=c.length-1-b,e=c[d];0===e.method.fullSignature.indexOf("java/lang/reflect/Method/invoke");){if(0===d)return null;e=c[--d]}return e.method.cls.getClassObject(a)}var Doppio=require("../doppiojvm"),util=Doppio.VM.Util,ThreadStatus=Doppio.VM.Enums.ThreadStatus,assert=Doppio.Debug.Assert,sun_reflect_ConstantPool=function(){function a(){}return a["getSize0(Ljava/lang/Object;)I"]=function(a,b,c){return a.throwNewException("Ljava/lang/UnsatisfiedLinkError;","Native method not implemented."),0},a["getClassAt0(Ljava/lang/Object;I)Ljava/lang/Class;"]=function(a,b,c,d){return a.throwNewException("Ljava/lang/UnsatisfiedLinkError;","Native method not implemented."),null},a["getClassAtIfLoaded0(Ljava/lang/Object;I)Ljava/lang/Class;"]=function(a,b,c,d){return a.throwNewException("Ljava/lang/UnsatisfiedLinkError;","Native method not implemented."),null},a["getMethodAt0(Ljava/lang/Object;I)Ljava/lang/reflect/Member;"]=function(a,b,c,d){return a.throwNewException("Ljava/lang/UnsatisfiedLinkError;","Native method not implemented."),null},a["getMethodAtIfLoaded0(Ljava/lang/Object;I)Ljava/lang/reflect/Member;"]=function(a,b,c,d){return a.throwNewException("Ljava/lang/UnsatisfiedLinkError;","Native method not implemented."),null},a["getFieldAt0(Ljava/lang/Object;I)Ljava/lang/reflect/Field;"]=function(a,b,c,d){return a.throwNewException("Ljava/lang/UnsatisfiedLinkError;","Native method not implemented."),null},a["getFieldAtIfLoaded0(Ljava/lang/Object;I)Ljava/lang/reflect/Field;"]=function(a,b,c,d){return a.throwNewException("Ljava/lang/UnsatisfiedLinkError;","Native method not implemented."),null},a["getMemberRefInfoAt0(Ljava/lang/Object;I)[Ljava/lang/String;"]=function(a,b,c,d){return a.throwNewException("Ljava/lang/UnsatisfiedLinkError;","Native method not implemented."),null},a["getIntAt0(Ljava/lang/Object;I)I"]=function(a,b,c,d){return c.get(d).value},a["getLongAt0(Ljava/lang/Object;I)J"]=function(a,b,c,d){return c.get(d).value},a["getFloatAt0(Ljava/lang/Object;I)F"]=function(a,b,c,d){return a.throwNewException("Ljava/lang/UnsatisfiedLinkError;","Native method not implemented."),0},a["getDoubleAt0(Ljava/lang/Object;I)D"]=function(a,b,c,d){return a.throwNewException("Ljava/lang/UnsatisfiedLinkError;","Native method not implemented."),0},a["getStringAt0(Ljava/lang/Object;I)Ljava/lang/String;"]=function(a,b,c,d){return a.throwNewException("Ljava/lang/UnsatisfiedLinkError;","Native method not implemented."),null},a["getUTF8At0(Ljava/lang/Object;I)Ljava/lang/String;"]=function(a,b,c,d){return util.initString(a.getBsCl(),c.get(d).value)},a}(),sun_reflect_NativeConstructorAccessorImpl=function(){function a(){}return a["newInstance0(Ljava/lang/reflect/Constructor;[Ljava/lang/Object;)Ljava/lang/Object;"]=function(a,b,c){var d=b["java/lang/reflect/Constructor/clazz"],e=b["java/lang/reflect/Constructor/slot"];a.setStatus(ThreadStatus.ASYNC_WAITING),d.$cls.initialize(a,function(b){if(null!==b){var d=b.getMethodFromSlot(e),f=new(b.getConstructor(a))(a),g=function(b){b?a.getBsCl().initializeClass(a,"Ljava/lang/reflect/InvocationTargetException;",function(c){if(null!==c){var d=new(c.getConstructor(a))(a);d["<init>(Ljava/lang/Throwable;)V"](a,[b],function(b){a.throwException(b?b:d)})}}):a.asyncReturn(f)};f[d.signature](a,c?c.array:null,g)}},!0)},a}(),sun_reflect_NativeMethodAccessorImpl=function(){function a(){}return a["invoke0(Ljava/lang/reflect/Method;Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;"]=function(a,b,c,d){var e=b["java/lang/reflect/Method/clazz"].$cls,f=b["java/lang/reflect/Method/slot"],g=b["java/lang/reflect/Method/returnType"],h=e.getMethodFromSlot(f),i=[],j=function(b,c){b?a.getBsCl().initializeClass(a,"Ljava/lang/reflect/InvocationTargetException;",function(c){if(null!==c){var d=new(c.getConstructor(a))(a);d["<init>(Ljava/lang/Throwable;)V"](a,[b],function(b){a.throwException(b?b:d)})}}):util.is_primitive_type(h.returnType)?"V"===h.returnType?a.asyncReturn(null):a.asyncReturn(g.$cls.createWrapperObject(a,c)):a.asyncReturn(c)};null!==d&&(i=util.unboxArguments(a,h.parameterTypes,d.array)),a.setStatus(ThreadStatus.ASYNC_WAITING),h.accessFlags.isStatic()?e.getConstructor(a)[h.fullSignature](a,i,j):c[h.signature](a,i,j)},a}(),sun_reflect_Reflection=function(){function a(){}return a["getCallerClass()Ljava/lang/Class;"]=function(a){return getCallerClass(a,2)},a["getClassAccessFlags(Ljava/lang/Class;)I"]=function(a,b){return b.$cls.accessFlags.getRawByte()},a["getCallerClass(I)Ljava/lang/Class;"]=getCallerClass,a}();registerNatives({"sun/reflect/ConstantPool":sun_reflect_ConstantPool,"sun/reflect/NativeConstructorAccessorImpl":sun_reflect_NativeConstructorAccessorImpl,"sun/reflect/NativeMethodAccessorImpl":sun_reflect_NativeMethodAccessorImpl,"sun/reflect/Reflection":sun_reflect_Reflection});
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uL3NyYy9uYXRpdmVzL3N1bl9yZWZsZWN0LnRzIl0sIm5hbWVzIjpbImdldENhbGxlckNsYXNzIiwic3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sIiwic3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sLmdldFNpemUwKExqYXZhL2xhbmcvT2JqZWN0OylJIiwic3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sLmdldENsYXNzQXQwKExqYXZhL2xhbmcvT2JqZWN0O0kpTGphdmEvbGFuZy9DbGFzczsiLCJzdW5fcmVmbGVjdF9Db25zdGFudFBvb2wuZ2V0Q2xhc3NBdElmTG9hZGVkMChMamF2YS9sYW5nL09iamVjdDtJKUxqYXZhL2xhbmcvQ2xhc3M7Iiwic3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sLmdldE1ldGhvZEF0MChMamF2YS9sYW5nL09iamVjdDtJKUxqYXZhL2xhbmcvcmVmbGVjdC9NZW1iZXI7Iiwic3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sLmdldE1ldGhvZEF0SWZMb2FkZWQwKExqYXZhL2xhbmcvT2JqZWN0O0kpTGphdmEvbGFuZy9yZWZsZWN0L01lbWJlcjsiLCJzdW5fcmVmbGVjdF9Db25zdGFudFBvb2wuZ2V0RmllbGRBdDAoTGphdmEvbGFuZy9PYmplY3Q7SSlMamF2YS9sYW5nL3JlZmxlY3QvRmllbGQ7Iiwic3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sLmdldEZpZWxkQXRJZkxvYWRlZDAoTGphdmEvbGFuZy9PYmplY3Q7SSlMamF2YS9sYW5nL3JlZmxlY3QvRmllbGQ7Iiwic3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sLmdldE1lbWJlclJlZkluZm9BdDAoTGphdmEvbGFuZy9PYmplY3Q7SSlbTGphdmEvbGFuZy9TdHJpbmc7Iiwic3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sLmdldEludEF0MChMamF2YS9sYW5nL09iamVjdDtJKUkiLCJzdW5fcmVmbGVjdF9Db25zdGFudFBvb2wuZ2V0TG9uZ0F0MChMamF2YS9sYW5nL09iamVjdDtJKUoiLCJzdW5fcmVmbGVjdF9Db25zdGFudFBvb2wuZ2V0RmxvYXRBdDAoTGphdmEvbGFuZy9PYmplY3Q7SSlGIiwic3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sLmdldERvdWJsZUF0MChMamF2YS9sYW5nL09iamVjdDtJKUQiLCJzdW5fcmVmbGVjdF9Db25zdGFudFBvb2wuZ2V0U3RyaW5nQXQwKExqYXZhL2xhbmcvT2JqZWN0O0kpTGphdmEvbGFuZy9TdHJpbmc7Iiwic3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sLmdldFVURjhBdDAoTGphdmEvbGFuZy9PYmplY3Q7SSlMamF2YS9sYW5nL1N0cmluZzsiLCJzdW5fcmVmbGVjdF9OYXRpdmVDb25zdHJ1Y3RvckFjY2Vzc29ySW1wbCIsInN1bl9yZWZsZWN0X05hdGl2ZUNvbnN0cnVjdG9yQWNjZXNzb3JJbXBsLm5ld0luc3RhbmNlMChMamF2YS9sYW5nL3JlZmxlY3QvQ29uc3RydWN0b3I7W0xqYXZhL2xhbmcvT2JqZWN0OylMamF2YS9sYW5nL09iamVjdDsiLCJzdW5fcmVmbGVjdF9OYXRpdmVNZXRob2RBY2Nlc3NvckltcGwiLCJzdW5fcmVmbGVjdF9OYXRpdmVNZXRob2RBY2Nlc3NvckltcGwuaW52b2tlMChMamF2YS9sYW5nL3JlZmxlY3QvTWV0aG9kO0xqYXZhL2xhbmcvT2JqZWN0O1tMamF2YS9sYW5nL09iamVjdDspTGphdmEvbGFuZy9PYmplY3Q7Iiwic3VuX3JlZmxlY3RfUmVmbGVjdGlvbiIsInN1bl9yZWZsZWN0X1JlZmxlY3Rpb24uZ2V0Q2FsbGVyQ2xhc3MoKUxqYXZhL2xhbmcvQ2xhc3M7Iiwic3VuX3JlZmxlY3RfUmVmbGVjdGlvbi5nZXRDbGFzc0FjY2Vzc0ZsYWdzKExqYXZhL2xhbmcvQ2xhc3M7KUkiXSwibWFwcGluZ3MiOiJBQW1NQSxRQUFBLGdCQUF3QixFQUFtQixHQUl6Q0EsSUFIQUEsR0FBSUEsR0FBU0EsRUFBT0EsZ0JBQ2xCQSxFQUFNQSxFQUFPQSxPQUFTQSxFQUFJQSxFQUMxQkEsRUFBMEJBLEVBQU9BLEdBQzhDQSxJ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QSxZQUFZQSxXQUNlQSxFQUFJQSxlQUFlQSxHQUFTQSxFQUFFQSxlQUFnQkEsRUFBUUEsRUFBTUEsR0FFNURBLEVBQUtBLEVBQUVBLFdBQVlBLEVBQVFBLEVBQU1BLElBR3RFRCxLQTRCQSx1QkFBQSxXQUFBRSxRQUFBQSxNQWNBQSxNQVpnQkEsR0FBQUEscUNBQWRBLFNBQWtEQSxHQUdoREMsTUFBT0EsZ0JBQWVBLEVBQVFBLElBS2xCRCxFQUFBQSwyQ0FBZEEsU0FBd0RBLEVBQW1CQSxHQUN6RUUsTUFBd0RBLEdBQVNBLEtBQU1BLFlBQVlBLGNBSHZFRixFQUFBQSxzQ0FBOEdBLGVBTTlIQSxJQUVBLGtCQUNFLDJCQUE0Qix5QkFDNUIsNENBQTZDLDBDQUM3Qyx1Q0FBd0MscUNBQ3hDLHlCQUEwQiIsImZpbGUiOiJzdW5fcmVmbGVjdC5qcyIsInNvdXJjZXNDb250ZW50IjpbImltcG9ydCBKVk1UeXBlcyA9IHJlcXVpcmUoJy4uLy4uL2luY2x1ZGVzL0pWTVR5cGVzJyk7XG5pbXBvcnQgKiBhcyBEb3BwaW8gZnJvbSAnLi4vZG9wcGlvanZtJztcbmltcG9ydCBKVk1UaHJlYWQgPSBEb3BwaW8uVk0uVGhyZWFkaW5nLkpWTVRocmVhZDtcbmltcG9ydCBSZWZlcmVuY2VDbGFzc0RhdGEgPSBEb3BwaW8uVk0uQ2xhc3NGaWxlLlJlZmVyZW5jZUNsYXNzRGF0YTtcbmltcG9ydCBsb2dnaW5nID0gRG9wcGlvLkRlYnVnLkxvZ2dpbmc7XG5pbXBvcnQgdXRpbCA9IERvcHBpby5WTS5VdGlsO1xuaW1wb3J0IENvbnN0YW50UG9vbCA9IERvcHBpby5WTS5DbGFzc0ZpbGUuQ29uc3RhbnRQb29sO1xuaW1wb3J0IExvbmcgPSBEb3BwaW8uVk0uTG9uZztcbmltcG9ydCBNZXRob2QgPSBEb3BwaW8uVk0uQ2xhc3NGaWxlLk1ldGhvZDtcbmltcG9ydCBUaHJlYWRTdGF0dXMgPSBEb3BwaW8uVk0uRW51bXMuVGhyZWFkU3RhdHVzO1xuaW1wb3J0IGFzc2VydCA9IERvcHBpby5EZWJ1Zy5Bc3NlcnQ7XG5pbXBvcnQgUHJpbWl0aXZlQ2xhc3NEYXRhID0gRG9wcGlvLlZNLkNsYXNzRmlsZS5QcmltaXRpdmVDbGFzc0RhdGE7XG5pbXBvcnQgSVN0YWNrVHJhY2VGcmFtZSA9IERvcHBpby5WTS5UaHJlYWRpbmcuSVN0YWNrVHJhY2VGcmFtZTtcbmRlY2xhcmUgdmFyIHJlZ2lzdGVyTmF0aXZlczogKGRlZnM6IGFueSkgPT4gdm9pZDtcblxuY2xhc3Mgc3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sIHtcblxuICBwdWJsaWMgc3RhdGljICdnZXRTaXplMChMamF2YS9sYW5nL09iamVjdDspSScodGhyZWFkOiBKVk1UaHJlYWQsIGphdmFUaGlzOiBKVk1UeXBlcy5zdW5fcmVmbGVjdF9Db25zdGFudFBvb2wsIGNwOiBDb25zdGFudFBvb2wuQ29uc3RhbnRQb29sKTogbnVtYmVyIHtcbiAgICB0aHJlYWQudGhyb3dOZXdFeGNlcHRpb24oJ0xqYXZhL2xhbmcvVW5zYXRpc2ZpZWRMaW5rRXJyb3I7JywgJ05hdGl2ZSBtZXRob2Qgbm90IGltcGxlbWVudGVkLicpO1xuICAgIC8vIFNhdGlzZnkgVHlwZVNjcmlwdCByZXR1cm4gdHlwZS5cbiAgICByZXR1cm4gMDtcbiAgfVxuXG4gIHB1YmxpYyBzdGF0aWMgJ2dldENsYXNzQXQwKExqYXZhL2xhbmcvT2JqZWN0O0kpTGphdmEvbGFuZy9DbGFzczsnKHRocmVhZDogSlZNVGhyZWFkLCBqYXZhVGhpczogSlZNVHlwZXMuc3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sLCBjcDogQ29uc3RhbnRQb29sLkNvbnN0YW50UG9vbCwgYXJnMTogbnVtYmVyKTogSlZNVHlwZXMuamF2YV9sYW5nX0NsYXNzIHtcbiAgICB0aHJlYWQudGhyb3dOZXdFeGNlcHRpb24oJ0xqYXZhL2xhbmcvVW5zYXRpc2ZpZWRMaW5rRXJyb3I7JywgJ05hdGl2ZSBtZXRob2Qgbm90IGltcGxlbWVudGVkLicpO1xuICAgIC8vIFNhdGlzZnkgVHlwZVNjcmlwdCByZXR1cm4gdHlwZS5cbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuXG4gIHB1YmxpYyBzdGF0aWMgJ2dldENsYXNzQXRJZkxvYWRlZDAoTGphdmEvbGFuZy9PYmplY3Q7SSlMamF2YS9sYW5nL0NsYXNzOycodGhyZWFkOiBKVk1UaHJlYWQsIGphdmFUaGlzOiBKVk1UeXBlcy5zdW5fcmVmbGVjdF9Db25zdGFudFBvb2wsIGNwOiBDb25zdGFudFBvb2wuQ29uc3RhbnRQb29sLCBhcmcxOiBudW1iZXIpOiBKVk1UeXBlcy5qYXZhX2xhbmdfQ2xhc3Mge1xuICAgIHRocmVhZC50aHJvd05ld0V4Y2VwdGlvbignTGphdmEvbGFuZy9VbnNhdGlzZmllZExpbmtFcnJvcjsnLCAnTmF0aXZlIG1ldGhvZCBub3QgaW1wbGVtZW50ZWQuJyk7XG4gICAgLy8gU2F0aXNmeSBUeXBlU2NyaXB0IHJldHVybiB0eXBlLlxuICAgIHJldHVybiBudWxsO1xuICB9XG5cbiAgcHVibGljIHN0YXRpYyAnZ2V0TWV0aG9kQXQwKExqYXZhL2xhbmcvT2JqZWN0O0kpTGphdmEvbGFuZy9yZWZsZWN0L01lbWJlcjsnKHRocmVhZDogSlZNVGhyZWFkLCBqYXZhVGhpczogSlZNVHlwZXMuc3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sLCBjcDogQ29uc3RhbnRQb29sLkNvbnN0YW50UG9vbCwgYXJnMTogbnVtYmVyKTogSlZNVHlwZXMuamF2YV9sYW5nX3JlZmxlY3RfTWVtYmVyIHtcbiAgICB0aHJlYWQudGhyb3dOZXdFeGNlcHRpb24oJ0xqYXZhL2xhbmcvVW5zYXRpc2ZpZWRMaW5rRXJyb3I7JywgJ05hdGl2ZSBtZXRob2Qgbm90IGltcGxlbWVudGVkLicpO1xuICAgIC8vIFNhdGlzZnkgVHlwZVNjcmlwdCByZXR1cm4gdHlwZS5cbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuXG4gIHB1YmxpYyBzdGF0aWMgJ2dldE1ldGhvZEF0SWZMb2FkZWQwKExqYXZhL2xhbmcvT2JqZWN0O0kpTGphdmEvbGFuZy9yZWZsZWN0L01lbWJlcjsnKHRocmVhZDogSlZNVGhyZWFkLCBqYXZhVGhpczogSlZNVHlwZXMuc3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sLCBjcDogQ29uc3RhbnRQb29sLkNvbnN0YW50UG9vbCwgYXJnMTogbnVtYmVyKTogSlZNVHlwZXMuamF2YV9sYW5nX3JlZmxlY3RfTWVtYmVyIHtcbiAgICB0aHJlYWQudGhyb3dOZXdFeGNlcHRpb24oJ0xqYXZhL2xhbmcvVW5zYXRpc2ZpZWRMaW5rRXJyb3I7JywgJ05hdGl2ZSBtZXRob2Qgbm90IGltcGxlbWVudGVkLicpO1xuICAgIC8vIFNhdGlzZnkgVHlwZVNjcmlwdCByZXR1cm4gdHlwZS5cbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuXG4gIHB1YmxpYyBzdGF0aWMgJ2dldEZpZWxkQXQwKExqYXZhL2xhbmcvT2JqZWN0O0kpTGphdmEvbGFuZy9yZWZsZWN0L0ZpZWxkOycodGhyZWFkOiBKVk1UaHJlYWQsIGphdmFUaGlzOiBKVk1UeXBlcy5zdW5fcmVmbGVjdF9Db25zdGFudFBvb2wsIGNwOiBDb25zdGFudFBvb2wuQ29uc3RhbnRQb29sLCBhcmcxOiBudW1iZXIpOiBKVk1UeXBlcy5qYXZhX2xhbmdfcmVmbGVjdF9GaWVsZCB7XG4gICAgdGhyZWFkLnRocm93TmV3RXhjZXB0aW9uKCdMamF2YS9sYW5nL1Vuc2F0aXNmaWVkTGlua0Vycm9yOycsICdOYXRpdmUgbWV0aG9kIG5vdCBpbXBsZW1lbnRlZC4nKTtcbiAgICAvLyBTYXRpc2Z5IFR5cGVTY3JpcHQgcmV0dXJuIHR5cGUuXG4gICAgcmV0dXJuIG51bGw7XG4gIH1cblxuICBwdWJsaWMgc3RhdGljICdnZXRGaWVsZEF0SWZMb2FkZWQwKExqYXZhL2xhbmcvT2JqZWN0O0kpTGphdmEvbGFuZy9yZWZsZWN0L0ZpZWxkOycodGhyZWFkOiBKVk1UaHJlYWQsIGphdmFUaGlzOiBKVk1UeXBlcy5zdW5fcmVmbGVjdF9Db25zdGFudFBvb2wsIGNwOiBDb25zdGFudFBvb2wuQ29uc3RhbnRQb29sLCBhcmcxOiBudW1iZXIpOiBKVk1UeXBlcy5qYXZhX2xhbmdfcmVmbGVjdF9GaWVsZCB7XG4gICAgdGhyZWFkLnRocm93TmV3RXhjZXB0aW9uKCdMamF2YS9sYW5nL1Vuc2F0aXNmaWVkTGlua0Vycm9yOycsICdOYXRpdmUgbWV0aG9kIG5vdCBpbXBsZW1lbnRlZC4nKTtcbiAgICAvLyBTYXRpc2Z5IFR5cGVTY3JpcHQgcmV0dXJuIHR5cGUuXG4gICAgcmV0dXJuIG51bGw7XG4gIH1cblxuICBwdWJsaWMgc3RhdGljICdnZXRNZW1iZXJSZWZJbmZvQXQwKExqYXZhL2xhbmcvT2JqZWN0O0kpW0xqYXZhL2xhbmcvU3RyaW5nOycodGhyZWFkOiBKVk1UaHJlYWQsIGphdmFUaGlzOiBKVk1UeXBlcy5zdW5fcmVmbGVjdF9Db25zdGFudFBvb2wsIGNwOiBDb25zdGFudFBvb2wuQ29uc3RhbnRQb29sLCBhcmcxOiBudW1iZXIpOiBKVk1UeXBlcy5KVk1BcnJheTxKVk1UeXBlcy5qYXZhX2xhbmdfU3RyaW5nPiB7XG4gICAgdGhyZWFkLnRocm93TmV3RXhjZXB0aW9uKCdMamF2YS9sYW5nL1Vuc2F0aXNmaWVkTGlua0Vycm9yOycsICdOYXRpdmUgbWV0aG9kIG5vdCBpbXBsZW1lbnRlZC4nKTtcbiAgICAvLyBTYXRpc2Z5IFR5cGVTY3JpcHQgcmV0dXJuIHR5cGUuXG4gICAgcmV0dXJuIG51bGw7XG4gIH1cblxuICBwdWJsaWMgc3RhdGljICdnZXRJbnRBdDAoTGphdmEvbGFuZy9PYmplY3Q7SSlJJyh0aHJlYWQ6IEpWTVRocmVhZCwgamF2YVRoaXM6IEpWTVR5cGVzLnN1bl9yZWZsZWN0X0NvbnN0YW50UG9vbCwgY3A6IENvbnN0YW50UG9vbC5Db25zdGFudFBvb2wsIGlkeDogbnVtYmVyKTogbnVtYmVyIHtcbiAgICByZXR1cm4gKDxDb25zdGFudFBvb2wuQ29uc3RJbnQzMj4gY3AuZ2V0KGlkeCkpLnZhbHVlO1xuICB9XG5cbiAgcHVibGljIHN0YXRpYyAnZ2V0TG9uZ0F0MChMamF2YS9sYW5nL09iamVjdDtJKUonKHRocmVhZDogSlZNVGhyZWFkLCBqYXZhVGhpczogSlZNVHlwZXMuc3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sLCBjcDogQ29uc3RhbnRQb29sLkNvbnN0YW50UG9vbCwgaWR4OiBudW1iZXIpOiBMb25nIHtcbiAgICByZXR1cm4gKDxDb25zdGFudFBvb2wuQ29uc3RMb25nPiBjcC5nZXQoaWR4KSkudmFsdWU7XG4gIH1cblxuICBwdWJsaWMgc3RhdGljICdnZXRGbG9hdEF0MChMamF2YS9sYW5nL09iamVjdDtJKUYnKHRocmVhZDogSlZNVGhyZWFkLCBqYXZhVGhpczogSlZNVHlwZXMuc3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sLCBjcDogQ29uc3RhbnRQb29sLkNvbnN0YW50UG9vbCwgYXJnMTogbnVtYmVyKTogbnVtYmVyIHtcbiAgICB0aHJlYWQudGhyb3dOZXdFeGNlcHRpb24oJ0xqYXZhL2xhbmcvVW5zYXRpc2ZpZWRMaW5rRXJyb3I7JywgJ05hdGl2ZSBtZXRob2Qgbm90IGltcGxlbWVudGVkLicpO1xuICAgIC8vIFNhdGlzZnkgVHlwZVNjcmlwdCByZXR1cm4gdHlwZS5cbiAgICByZXR1cm4gMDtcbiAgfVxuXG4gIHB1YmxpYyBzdGF0aWMgJ2dldERvdWJsZUF0MChMamF2YS9sYW5nL09iamVjdDtJKUQnKHRocmVhZDogSlZNVGhyZWFkLCBqYXZhVGhpczogSlZNVHlwZXMuc3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sLCBjcDogQ29uc3RhbnRQb29sLkNvbnN0YW50UG9vbCwgYXJnMTogbnVtYmVyKTogbnVtYmVyIHtcbiAgICB0aHJlYWQudGhyb3dOZXdFeGNlcHRpb24oJ0xqYXZhL2xhbmcvVW5zYXRpc2ZpZWRMaW5rRXJyb3I7JywgJ05hdGl2ZSBtZXRob2Qgbm90IGltcGxlbWVudGVkLicpO1xuICAgIC8vIFNhdGlzZnkgVHlwZVNjcmlwdCByZXR1cm4gdHlwZS5cbiAgICByZXR1cm4gMDtcbiAgfVxuXG4gIHB1YmxpYyBzdGF0aWMgJ2dldFN0cmluZ0F0MChMamF2YS9sYW5nL09iamVjdDtJKUxqYXZhL2xhbmcvU3RyaW5nOycodGhyZWFkOiBKVk1UaHJlYWQsIGphdmFUaGlzOiBKVk1UeXBlcy5zdW5fcmVmbGVjdF9Db25zdGFudFBvb2wsIGNwOiBDb25zdGFudFBvb2wuQ29uc3RhbnRQb29sLCBhcmcxOiBudW1iZXIpOiBKVk1UeXBlcy5qYXZhX2xhbmdfU3RyaW5nIHtcbiAgICB0aHJlYWQudGhyb3dOZXdFeGNlcHRpb24oJ0xqYXZhL2xhbmcvVW5zYXRpc2ZpZWRMaW5rRXJyb3I7JywgJ05hdGl2ZSBtZXRob2Qgbm90IGltcGxlbWVudGVkLicpO1xuICAgIC8vIFNhdGlzZnkgVHlwZVNjcmlwdCByZXR1cm4gdHlwZS5cbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuXG4gIHB1YmxpYyBzdGF0aWMgJ2dldFVURjhBdDAoTGphdmEvbGFuZy9PYmplY3Q7SSlMamF2YS9sYW5nL1N0cmluZzsnKHRocmVhZDogSlZNVGhyZWFkLCBqYXZhVGhpczogSlZNVHlwZXMuc3VuX3JlZmxlY3RfQ29uc3RhbnRQb29sLCBjcDogQ29uc3RhbnRQb29sLkNvbnN0YW50UG9vbCwgaWR4OiBudW1iZXIpOiBKVk1UeXBlcy5qYXZhX2xhbmdfU3RyaW5nIHtcbiAgICByZXR1cm4gdXRpbC5pbml0U3RyaW5nKHRocmVhZC5nZXRCc0NsKCksICg8Q29uc3RhbnRQb29sLkNvbnN0VVRGOD4gY3AuZ2V0KGlkeCkpLnZhbHVlKTtcbiAgfVxuXG59XG5cbmNsYXNzIHN1bl9yZWZsZWN0X05hdGl2ZUNvbnN0cnVjdG9yQWNjZXNzb3JJbXBsIHtcblxuICBwdWJsaWMgc3RhdGljICduZXdJbnN0YW5jZTAoTGphdmEvbGFuZy9yZWZsZWN0L0NvbnN0cnVjdG9yO1tMamF2YS9sYW5nL09iamVjdDspTGphdmEvbGFuZy9PYmplY3Q7Jyh0aHJlYWQ6IEpWTVRocmVhZCwgbTogSlZNVHlwZXMuamF2YV9sYW5nX3JlZmxlY3RfQ29uc3RydWN0b3IsIHBhcmFtczogSlZNVHlwZXMuSlZNQXJyYXk8SlZNVHlwZXMuamF2YV9sYW5nX09iamVjdD4pOiB2b2lkIHtcbiAgICB2YXIgY2xzID0gbVsnamF2YS9sYW5nL3JlZmxlY3QvQ29uc3RydWN0b3IvY2xhenonXSxcbiAgICAgIHNsb3QgPSBtWydqYXZhL2xhbmcvcmVmbGVjdC9Db25zdHJ1Y3Rvci9zbG90J107XG4gICAgdGhyZWFkLnNldFN0YXR1cyhUaHJlYWRTdGF0dXMuQVNZTkNfV0FJVElORyk7XG4gICAgY2xzLiRjbHMuaW5pdGlhbGl6ZSh0aHJlYWQsIChjbHM6IFJlZmVyZW5jZUNsYXNzRGF0YTxKVk1UeXBlcy5qYXZhX2xhbmdfT2JqZWN0PikgPT4ge1xuICAgICAgaWYgKGNscyAhPT0gbnVsbCkge1xuICAgICAgICB2YXIgbWV0aG9kOiBNZXRob2QgPSBjbHMuZ2V0TWV0aG9kRnJvbVNsb3Qoc2xvdCksXG4gICAgICAgICAgb2JqID0gbmV3IChjbHMuZ2V0Q29uc3RydWN0b3IodGhyZWFkKSkodGhyZWFkKSwgaTogbnVtYmVyLFxuICAgICAgICAgIGNiID0gKGU/OiBKVk1UeXBlcy5qYXZhX2xhbmdfVGhyb3dhYmxlKSA9PiB7XG4gICAgICAgICAgICBpZiAoZSkge1xuICAgICAgICAgICAgICAvLyBXcmFwIGluIGEgamF2YS5sYW5nLnJlZmxlY3QuSW52b2NhdGlvblRhcmdldEV4Y2VwdGlvblxuICAgICAgICAgICAgICB0aHJlYWQuZ2V0QnNDbCgpLmluaXRpYWxpemVDbGFzcyh0aHJlYWQsICdMamF2YS9sYW5nL3JlZmxlY3QvSW52b2NhdGlvblRhcmdldEV4Y2VwdGlvbjsnLCAoY2RhdGE6IFJlZmVyZW5jZUNsYXNzRGF0YTxKVk1UeXBlcy5qYXZhX2xhbmdfcmVmbGVjdF9JbnZvY2F0aW9uVGFyZ2V0RXhjZXB0aW9uPikgPT4ge1xuICAgICAgICAgICAgICAgIGlmIChjZGF0YSAhPT0gbnVsbCkge1xuICAgICAgICAgICAgICAgICAgdmFyIHdyYXBwZWRFID0gbmV3IChjZGF0YS5nZXRDb25zdHJ1Y3Rvcih0aHJlYWQpKSh0aHJlYWQpO1xuICAgICAgICAgICAgICAgICAgd3JhcHBlZEVbJzxpbml0PihMamF2YS9sYW5nL1Rocm93YWJsZTspViddKHRocmVhZCwgW2VdLCAoZT86IEpWTVR5cGVzLmphdmFfbGFuZ19UaHJvd2FibGUpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgdGhyZWFkLnRocm93RXhjZXB0aW9uKGUgPyBlIDogd3JhcHBlZEUpO1xuICAgICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgIC8vIHJ2IGlzIG5vdCBkZWZpbmVkLCBzaW5jZSBjb25zdHJ1Y3RvcnMgZG8gbm90IHJldHVybiBhIHZhbHVlLlxuICAgICAgICAgICAgICAvLyBSZXR1cm4gdGhlIG9iamVjdCB3ZSBwYXNzZWQgdG8gdGhlIGNvbnN0cnVjdG9yLlxuICAgICAgICAgICAgICB0aHJlYWQuYXN5bmNSZXR1cm4ob2JqKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9O1xuXG4gICAgICAgIGFzc2VydChzbG90ID49IDAsIFwiRm91bmQgYSBjb25zdHJ1Y3RvciB3aXRob3V0IGEgc2xvdD8hXCIpO1xuICAgICAgICAoPEpWTVR5cGVzLkpWTUZ1bmN0aW9uPiAoPGFueT4gb2JqKVttZXRob2Quc2lnbmF0dXJlXSkodGhyZWFkLCBwYXJhbXMgPyBwYXJhbXMuYXJyYXkgOiBudWxsLCBjYik7XG4gICAgICB9XG4gICAgfSwgdHJ1ZSk7XG4gIH1cblxufVxuXG5jbGFzcyBzdW5fcmVmbGVjdF9OYXRpdmVNZXRob2RBY2Nlc3NvckltcGwge1xuXG4gIC8qKlxuICAgKiBJbnZva2UgdGhlIHNwZWNpZmllZCBtZXRob2Qgb24gdGhlIGdpdmVuIG9iamVjdCB3aXRoIHRoZSBnaXZlbiBwYXJhbWV0ZXJzLlxuICAgKiBJZiB0aGUgbWV0aG9kIGlzIGFuIGludGVyZmFjZSBtZXRob2QsIHBlcmZvcm0gYSB2aXJ0dWFsIG1ldGhvZCBkaXNwYXRjaC5cbiAgICovXG4gIHB1YmxpYyBzdGF0aWMgJ2ludm9rZTAoTGphdmEvbGFuZy9yZWZsZWN0L01ldGhvZDtMamF2YS9sYW5nL09iamVjdDtbTGphdmEvbGFuZy9PYmplY3Q7KUxqYXZhL2xhbmcvT2JqZWN0OycodGhyZWFkOiBKVk1UaHJlYWQsIG1PYmo6IEpWTVR5cGVzLmphdmFfbGFuZ19yZWZsZWN0X01ldGhvZCwgb2JqOiBKVk1UeXBlcy5qYXZhX2xhbmdfT2JqZWN0LCBwYXJhbXM6IEpWTVR5cGVzLkpWTUFycmF5PEpWTVR5cGVzLmphdmFfbGFuZ19PYmplY3Q+KTogdm9pZCB7XG4gICAgdmFyIGNscyA9IDxSZWZlcmVuY2VDbGFzc0RhdGE8SlZNVHlwZXMuamF2YV9sYW5nX09iamVjdD4+IG1PYmpbJ2phdmEvbGFuZy9yZWZsZWN0L01ldGhvZC9jbGF6eiddLiRjbHMsXG4gICAgICBzbG90OiBudW1iZXIgPSBtT2JqWydqYXZhL2xhbmcvcmVmbGVjdC9NZXRob2Qvc2xvdCddLFxuICAgICAgcmV0VHlwZSA9IG1PYmpbJ2phdmEvbGFuZy9yZWZsZWN0L01ldGhvZC9yZXR1cm5UeXBlJ10sXG4gICAgICBtOiBNZXRob2QgPSBjbHMuZ2V0TWV0aG9kRnJvbVNsb3Qoc2xvdCksXG4gICAgICBhcmdzOiBhbnlbXSA9IFtdLFxuICAgICAgY2IgPSAoZT86IEpWTVR5cGVzLmphdmFfbGFuZ19UaHJvd2FibGUsIHJ2PzogYW55KSA9PiB7XG4gICAgICAgIGlmIChlKSB7XG4gICAgICAgICAgLy8gV3JhcCBpbiBhIGphdmEubGFuZy5yZWZsZWN0Lkludm9jYXRpb25UYXJnZXRFeGNlcHRpb25cbiAgICAgICAgICB0aHJlYWQuZ2V0QnNDbCgpLmluaXRpYWxpemVDbGFzcyh0aHJlYWQsICdMamF2YS9sYW5nL3JlZmxlY3QvSW52b2NhdGlvblRhcmdldEV4Y2VwdGlvbjsnLCAoY2RhdGE6IFJlZmVyZW5jZUNsYXNzRGF0YTxKVk1UeXBlcy5qYXZhX2xhbmdfcmVmbGVjdF9JbnZvY2F0aW9uVGFyZ2V0RXhjZXB0aW9uPikgPT4ge1xuICAgICAgICAgICAgaWYgKGNkYXRhICE9PSBudWxsKSB7XG4gICAgICAgICAgICAgIHZhciB3cmFwcGVkRSA9IG5ldyAoY2RhdGEuZ2V0Q29uc3RydWN0b3IodGhyZWFkKSkodGhyZWFkKTtcbiAgICAgICAgICAgICAgd3JhcHBlZEVbJzxpbml0PihMamF2YS9sYW5nL1Rocm93YWJsZTspViddKHRocmVhZCwgW2VdLCAoZT86IEpWTVR5cGVzLmphdmFfbGFuZ19UaHJvd2FibGUpID0+IHtcbiAgICAgICAgICAgICAgICB0aHJlYWQudGhyb3dFeGNlcHRpb24oZSA/IGUgOiB3cmFwcGVkRSk7XG4gICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH0pO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIGlmICh1dGlsLmlzX3ByaW1pdGl2ZV90eXBlKG0ucmV0dXJuVHlwZSkpIHtcbiAgICAgICAgICAgIGlmIChtLnJldHVyblR5cGUgPT09ICdWJykge1xuICAgICAgICAgICAgICAvLyBhcHBhcmVudGx5IHRoZSBKVk0gcmV0dXJucyBOVUxMIHdoZW4gdGhlcmUncyBhIHZvaWQgcmV0dXJuIHZhbHVlLFxuICAgICAgICAgICAgICAvLyByYXRoZXIgdGhhbiBhdXRvYm94aW5nIGEgVm9pZCBvYmplY3QuIEdvIGZpZ3VyZSFcbiAgICAgICAgICAgICAgdGhyZWFkLmFzeW5jUmV0dXJuKG51bGwpO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgLy8gd3JhcCB1cCBwcmltaXRpdmVzIGluIHRoZWlyIE9iamVjdCBib3hcbiAgICAgICAgICAgICAgdGhyZWFkLmFzeW5jUmV0dXJuKCg8UHJpbWl0aXZlQ2xhc3NEYXRhPiByZXRUeXBlLiRjbHMpLmNyZWF0ZVdyYXBwZXJPYmplY3QodGhyZWFkLCBydikpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICB0aHJlYWQuYXN5bmNSZXR1cm4ocnYpO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfTtcblxuICAgIGlmIChwYXJhbXMgIT09IG51bGwpIHtcbiAgICAgIGFyZ3MgPSB1dGlsLnVuYm94QXJndW1lbnRzKHRocmVhZCwgbS5wYXJhbWV0ZXJUeXBlcywgcGFyYW1zLmFycmF5KVxuICAgIH1cblxuICAgIHRocmVhZC5zZXRTdGF0dXMoVGhyZWFkU3RhdHVzLkFTWU5DX1dBSVRJTkcpO1xuICAgIGlmIChtLmFjY2Vzc0ZsYWdzLmlzU3RhdGljKCkpIHtcbiAgICAgICg8SlZNVHlwZXMuSlZNRnVuY3Rpb24+ICg8YW55PiBjbHMuZ2V0Q29uc3RydWN0b3IodGhyZWFkKSlbbS5mdWxsU2lnbmF0dXJlXSkodGhyZWFkLCBhcmdzLCBjYik7XG4gICAgfSBlbHNlIHtcbiAgICAgICg8SlZNVHlwZXMuSlZNRnVuY3Rpb24+ICg8YW55PiBvYmopW20uc2lnbmF0dXJlXSkodGhyZWFkLCBhcmdzLCBjYik7XG4gICAgfVxuICB9XG59XG5cbi8qKlxuICogRnJvbSBKREsgZG9jdW1lbnRhdGlvbjpcbiAqICAgUmV0dXJucyB0aGUgY2xhc3Mgb2YgdGhlIG1ldGhvZCByZWFsRnJhbWVzVG9Ta2lwIGZyYW1lcyB1cCB0aGUgc3RhY2tcbiAqICAgKHplcm8tYmFzZWQpLCBpZ25vcmluZyBmcmFtZXMgYXNzb2NpYXRlZCB3aXRoXG4gKiAgIGphdmEubGFuZy5yZWZsZWN0Lk1ldGhvZC5pbnZva2UoKSBhbmQgaXRzIGltcGxlbWVudGF0aW9uLiBUaGUgZmlyc3RcbiAqICAgZnJhbWUgaXMgdGhhdCBhc3NvY2lhdGVkIHdpdGggdGhpcyBtZXRob2QsIHNvIGdldENhbGxlckNsYXNzKDApIHJldHVybnNcbiAqICAgdGhlIENsYXNzIG9iamVjdCBmb3Igc3VuLnJlZmxlY3QuUmVmbGVjdGlvbi4gRnJhbWVzIGFzc29jaWF0ZWQgd2l0aFxuICogICBqYXZhLmxhbmcucmVmbGVjdC5NZXRob2QuaW52b2tlKCkgYW5kIGl0cyBpbXBsZW1lbnRhdGlvbiBhcmUgY29tcGxldGVseVxuICogICBpZ25vcmVkIGFuZCBkbyBub3QgY291bnQgdG93YXJkIHRoZSBudW1iZXIgb2YgXCJyZWFsXCIgZnJhbWVzIHNraXBwZWQuXG4gKi9cbmZ1bmN0aW9uIGdldENhbGxlckNsYXNzKHRocmVhZDogSlZNVGhyZWFkLCBmcmFtZXNUb1NraXA6IG51bWJlcik6IEpWTVR5cGVzLmphdmFfbGFuZ19DbGFzcyB7XG4gIHZhciBjYWxsZXIgPSB0aHJlYWQuZ2V0U3RhY2tUcmFjZSgpLFxuICAgIGlkeCA9IGNhbGxlci5sZW5ndGggLSAxIC0gZnJhbWVzVG9Ta2lwLFxuICAgIGZyYW1lOiBJU3RhY2tUcmFjZUZyYW1lID0gY2FsbGVyW2lkeF07XG4gIHdoaWxlIChmcmFtZS5tZXRob2QuZnVsbFNpZ25hdHVyZS5pbmRleE9mKCdqYXZhL2xhbmcvcmVmbGVjdC9NZXRob2QvaW52b2tlJykgPT09IDApIHtcbiAgICBpZiAoaWR4ID09PSAwKSB7XG4gICAgICAvLyBObyBtb3JlIHN0YWNrIHRvIHNlYXJjaCFcbiAgICAgIC8vIFhYWDogV2hhdCBkb2VzIHRoZSBKREsgZG8gaGVyZSwgdGhyb3cgYW4gZXhjZXB0aW9uP1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICAgIGZyYW1lID0gY2FsbGVyWy0taWR4XTtcbiAgfVxuXG4gIHJldHVybiBmcmFtZS5tZXRob2QuY2xzLmdldENsYXNzT2JqZWN0KHRocmVhZCk7XG59XG5cbmNsYXNzIHN1bl9yZWZsZWN0X1JlZmxlY3Rpb24ge1xuXG4gIHB1YmxpYyBzdGF0aWMgJ2dldENhbGxlckNsYXNzKClMamF2YS9sYW5nL0NsYXNzOycodGhyZWFkOiBKVk1UaHJlYWQpOiBKVk1UeXBlcy5qYXZhX2xhbmdfQ2xhc3Mge1xuICAgIC8vIDB0aCBpdGVtIGlzIFJlZmxlY3Rpb24gY2xhc3MsIDFzdCBpdGVtIGlzIHRoZSBjbGFzcyB0aGF0IGNhbGxlZCB1cyxcbiAgICAvLyBhbmQgMm5kIGl0ZW0gaXMgdGhlIGNhbGxlciBvZiBvdXIgY2FsbGVyLCB3aGljaCBpcyBjb3JyZWN0LlxuICAgIHJldHVybiBnZXRDYWxsZXJDbGFzcyh0aHJlYWQsIDIpO1xuICB9XG5cbiAgcHVibGljIHN0YXRpYyAnZ2V0Q2FsbGVyQ2xhc3MoSSlMamF2YS9sYW5nL0NsYXNzOyc6ICh0aHJlYWQ6IEpWTVRocmVhZCwgZnJhbWVzVG9Ta2lwOiBudW1iZXIpID0+IEpWTVR5cGVzLmphdmFfbGFuZ19DbGFzcyA9IGdldENhbGxlckNsYXNzO1xuXG4gIHB1YmxpYyBzdGF0aWMgJ2dldENsYXNzQWNjZXNzRmxhZ3MoTGphdmEvbGFuZy9DbGFzczspSScodGhyZWFkOiBKVk1UaHJlYWQsIGNsYXNzT2JqOiBKVk1UeXBlcy5qYXZhX2xhbmdfQ2xhc3MpOiBudW1iZXIge1xuICAgIHJldHVybiAoPFJlZmVyZW5jZUNsYXNzRGF0YTxKVk1UeXBlcy5qYXZhX2xhbmdfT2JqZWN0Pj4gY2xhc3NPYmouJGNscykuYWNjZXNzRmxhZ3MuZ2V0UmF3Qnl0ZSgpO1xuICB9XG5cbn1cblxucmVnaXN0ZXJOYXRpdmVzKHtcbiAgJ3N1bi9yZWZsZWN0L0NvbnN0YW50UG9vbCc6IHN1bl9yZWZsZWN0X0NvbnN0YW50UG9vbCxcbiAgJ3N1bi9yZWZsZWN0L05hdGl2ZUNvbnN0cnVjdG9yQWNjZXNzb3JJbXBsJzogc3VuX3JlZmxlY3RfTmF0aXZlQ29uc3RydWN0b3JBY2Nlc3NvckltcGwsXG4gICdzdW4vcmVmbGVjdC9OYXRpdmVNZXRob2RBY2Nlc3NvckltcGwnOiBzdW5fcmVmbGVjdF9OYXRpdmVNZXRob2RBY2Nlc3NvckltcGwsXG4gICdzdW4vcmVmbGVjdC9SZWZsZWN0aW9uJzogc3VuX3JlZmxlY3RfUmVmbGVjdGlvblxufSk7XG4iXX0=