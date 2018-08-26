package com.ml.mlServiceConsumer.exceptionparser;

public class ParseException extends Exception {

	private static final long serialVersionUID = -5789847648899123328L;

	public ParseException(final String message) {
		super(message);
	}

	public ParseException(final String message, final Throwable e) {
		super(message, e);
	}
}
