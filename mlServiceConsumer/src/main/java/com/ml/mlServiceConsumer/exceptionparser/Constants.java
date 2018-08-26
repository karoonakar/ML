package com.ml.mlServiceConsumer.exceptionparser;

public class Constants {
	
	public static final String CLAZZ = "((?:[\\w\\s](?:\\$+|\\.|/)?)+)";
	public static final String METHOD = "\\.([\\w|_|\\$|\\s|<|>]+)";
	public static final String EXCEPTION_CLAZZ = "((?:\\w(?:\\$+|\\.|/)?)+)";
	public static final String EXCEPTION = "(" + EXCEPTION_CLAZZ + "(?:Exception|Error))";
	public static final String SOURCEC_CHARS = "[^\\(\\)]+";
	public static final String SOURCE = "\\((" + SOURCEC_CHARS + "(?:\\([^\\)]*\\))?)\\)";
	public static final String FRAME = "(?:\\s*at\\s+)" + CLAZZ + METHOD + "\\s*" + SOURCE;
	public static final String CAUSE = "((?:\\s*...\\s+\\d+\\s+more)?\\s+Caused\\s+by:\\s+)" + EXCEPTION;
	public static final String CAUSED_BY ="Caused by:(.*?:[^:]+):";
}
