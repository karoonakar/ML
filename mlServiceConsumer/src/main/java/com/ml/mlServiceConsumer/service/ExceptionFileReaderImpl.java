package com.ml.mlServiceConsumer.service;

import java.util.Scanner;

import com.ml.mlServiceConsumer.exceptionparser.StackTraceParser;


public class ExceptionFileReaderImpl implements ExceptionFileReader{

	

	@Override
	public void findAllStackTraceFromFile() {
		String filePath="stack1.txt";
		String logTest=readLogFile(filePath);
		StackTraceParser StackTraceParser = new StackTraceParser(logTest); 
		
	}
	
	private String readLogFile(String path) {
		StringBuilder output = new StringBuilder();
		Scanner scanner = new Scanner(getClass().getResourceAsStream(path), "UTF-8");
		while(scanner.hasNextLine()) {
			String s = scanner.nextLine();
			output.append(s + "\n");
		}
		return output.toString();
	}
	
}
