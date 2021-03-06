package com.ml.mlServiceConsumer.exceptionparser;

import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.google.common.collect.Lists;


public class StackTraceParser {
	
	private static final Pattern exceptionPattern = Pattern.compile(Constants.EXCEPTION);
	private static final Pattern framePattern = Pattern.compile(Constants.FRAME);
	private static final Pattern causePattern = Pattern.compile(Constants.CAUSE);

	private final String text;
	private int currentIndex = 0;
	private String exceptionType;
	private String message;
	private List<StackTraceElement> frames;
	private final List<StackTraceMatch> traces = Lists.newLinkedList();
	private int currentStackTraceStart = -1;
	private String rawInput;
	private boolean hasSubMatch;

	public StackTraceParser(final String text) {
		rawInput = text;
		this.text = preprocessString(text);
		doParsing();
	}

	private void doParsing() {
		do {
			StackTrace trace = findStackTrace();
			if (trace != null) {
				traces.add(new StackTraceMatch(trace, currentStackTraceStart, currentIndex));
			}
			currentStackTraceStart = -1;
		} while (hasSubMatch);
	}

	private StackTrace findStackTrace() {
		resetVariables();
		if (findExceptionBeforeFrame()) {
			hasSubMatch = true;
			if (hasMessage()) {
				parseMessage();
			}
			while (findFrame()) {
			}
			if (frames.size() > 0) {
				StackTrace result = new StackTrace(exceptionType, message, frames);
				if (hasCause()) {
					final StackTrace cause = findStackTrace();
					result = new StackTrace(result.getExceptionType(), result.getMessage(), result.getElements(), cause);
				}
				return result;
			}
		}
		return null;
	}

	private void resetVariables() {
		exceptionType = null;
		message = null;
		hasSubMatch = false;
		frames = Lists.newLinkedList();
	}

	private int numberOfLeadingWhiteSpaces(String text) {
		int c = 0;
		for (int i = 0; i < text.length(); i++) {
			if (text.charAt(i) == ' ')
				c++;
			else
				return c;
		}
		return c;
	}

	private boolean findExceptionBeforeFrame() {
		int frameIndex = currentIndex;

		Matcher frameMatcher = framePattern.matcher(text);
		while (frameMatcher.find(frameIndex)) {
			int frameStart = frameMatcher.start();
			int whiteSpaces = numberOfLeadingWhiteSpaces(text.substring(frameStart, frameMatcher.end()));
			Matcher subFrameMatcher = framePattern.matcher(text.substring(frameStart + whiteSpaces + 1, frameMatcher.end()));
			if (subFrameMatcher.find()) {
				frameIndex = frameStart + whiteSpaces + 1 + subFrameMatcher.start();
				continue;
			}

			if (!hasAcceptableWhiteSpaceCount(frameMatcher)) {
				frameIndex = frameMatcher.end();
				continue;
			}

			int exceptionStart = -1;
			int exceptionEnd = -1;
			final Matcher matcher = exceptionPattern.matcher(text);
			while (currentIndex < frameStart && matcher.find(currentIndex)) {
				if (matcher.start() > frameStart)
					break;
				currentIndex = matcher.end();
				String potentialMessage = text.substring(matcher.end(), frameStart).trim();
				if (!potentialMessage.isEmpty() && !potentialMessage.startsWith(":")) {
					continue;
				}
				exceptionType = matcher.group().replaceAll("/", ".");
				exceptionStart = matcher.start();
				exceptionEnd = matcher.end();
			}
			if (exceptionStart >= 0) {
				setStackTraceStart(exceptionStart);
				currentIndex = exceptionEnd;
				return true;
			}
			frameIndex = frameMatcher.end();
			currentIndex = frameMatcher.end();
		}
		return false;

	}

	private void setStackTraceStart(int start) {
		if (currentStackTraceStart < 0)
			currentStackTraceStart = start;
	}

	private boolean hasMessage() {
		return currentIndex < text.length() && text.charAt(currentIndex) == ':';
	}

	private void parseMessage() {
		final Matcher matcher = framePattern.matcher(text);
		if (matcher.find(currentIndex)) {
			final int messageStart = currentIndex + 1;
			final int messageEnd = matcher.start();
			message = text.substring(messageStart, messageEnd).trim();
			currentIndex = messageEnd;
		}
	}

	private boolean findFrame() {
		final Matcher matcher = framePattern.matcher(text);
		if (matcher.find(currentIndex) && matcher.start() == currentIndex && hasAcceptableWhiteSpaceCount(matcher)) {
			final String method = (matcher.group(1).replaceAll("/", ".") + "." + matcher.group(2)).replaceAll("\\s", "");
			final String source = matcher.group(3);
			frames.add(new StackTraceElement(method, source));
			currentIndex = matcher.end();
			return true;
		}
		return false;
	}

	private boolean hasAcceptableWhiteSpaceCount(Matcher matcher) {
		String potentialMethod = (matcher.group(1) + matcher.group(2)).trim().replaceAll("\\s+", " ");
		int whiteSpaces = potentialMethod.replaceAll("[^\\s]", "").length();
		if (whiteSpaces == 0)
			return true;
		else
			return (potentialMethod.length() - whiteSpaces) / (float) whiteSpaces > 20;
	}

	private boolean hasCause() {
		final Matcher matcher = causePattern.matcher(text);
		if (matcher.find(currentIndex) && matcher.start() == currentIndex) {
			currentIndex = matcher.end(1);
			return true;
		}
		return false;
	}

	public List<StackTrace> getStackTraces() {
		List<StackTrace> result = Lists.newLinkedList();
		for (StackTraceMatch match : traces) {
			result.add(match.stackTrace);
		}
		return result;
	}

	public List<StackTraceMatch> getMatches() {
		return traces;
	}

	private String preprocessString(final String text) {
		final String[] lines = text.replaceAll("\\r", "").replaceAll("\t", " ").split("\\n");
		final StringBuilder builder = new StringBuilder();
		for (int i = 0; i < lines.length; i++) {
			if (i > 0)
				builder.append(" ");
			builder.append(lines[i]);
		}
		return builder.toString();
	}

	public String substring(int startIndex, int endIndex) {
		endIndex = Math.min(endIndex, text.length());
		return rawInput.replaceAll("\\r", "").substring(startIndex, endIndex).replaceAll("\\n", "\r\n");
	}

	public StackTrace parse(final String text) throws ParseException {
		final List<StackTrace> result = this.parseAll(text);
		if (result.size() == 1) {
			return result.get(0);
		} else {
			throw new ParseException(
					"Can't match exactly one stacktrace in given String. Matches: "
							+ result.size()
							+ " stacktraces.");
		}
	}

	public List<StackTrace> parseAll(final String text) {
		final StackTraceParser parser = new StackTraceParser(text);
		return parser.getStackTraces();
	}

	public static class StackTraceMatch {

		private StackTrace stackTrace;
		private int startIndex;
		private int endIndex;

		public StackTraceMatch(StackTrace stackTrace, int startIndex, int endIndex) {
			this.stackTrace = stackTrace;
			this.startIndex = startIndex;
			this.endIndex = endIndex;
		}

		public StackTrace getStackTrace() {
			return stackTrace;
		}

		public int getStartIndex() {
			return startIndex;
		}

		public int getEndIndex() {
			return endIndex;
		}
	}
}