package com.example;

/**
 * this template is meant to allow compilation to multiple architectures
 * @author Gabriel Lacey
 */

public interface Assembler {
	/**
     * @return name of computer
     */
	public String getName();
	/**
     * @param input tokenized source assembly
	 * @param outputFile name of binary file to output to
     */
	public Error assemble(ArrayList<ArrayList<String>> input, String outputFile);
	/**
	 * 
	 * @return the opp codes supported by the assembler
	 */
	public String[] supportedOps();
}
