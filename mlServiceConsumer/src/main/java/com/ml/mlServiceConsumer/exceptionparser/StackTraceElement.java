package com.ml.mlServiceConsumer.exceptionparser;


public class StackTraceElement {

	private String method;
	private String source;

	protected StackTraceElement() {
		// for deserialization
	}

	public StackTraceElement(final String method) {
		this(method, null);
	}

	public StackTraceElement(final String method, final String source) {
		this.method = method;
		this.source = source;
	}

	public String getMethod() {
		return method;
	}

	public String getSource() {
		return source;
	}

	@Override
	public String toString() {
		return String.format("at %s(%s)", method, getSource() == null ? "" : getSource());
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((method == null) ? 0 : method.hashCode());
		result = prime * result + ((source == null) ? 0 : source.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		StackTraceElement other = (StackTraceElement) obj;
		if (method == null) {
			if (other.method != null)
				return false;
		} else if (!method.equals(other.method))
			return false;
		if (source == null) {
			if (other.source != null)
				return false;
		} else if (!source.equals(other.source))
			return false;
		return true;
	}
}