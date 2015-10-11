/**
 * Calculates the maximum integer in input.txt 
 * 
 * 
 */
package com.tinkeracademy.ap;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Main {

	public static void main(String[] args) throws FileNotFoundException {
		Scanner s = new Scanner(new File("input.txt"));
		/*
		 *  Local Variable max will hold the maximum value
		 */
		int max = 0;
		for (int i = 0; i < 10000; i++) {
			/* 
			 * Local Variable will hold the next integer read from input file
			 */
			int next = s.nextInt();
			if (next > max) {
				/* 
				 * TODO Add your code below
				 * 
				 * What should happen if next > max?
				 */
			}
			
		}
		System.out.println("max="+max);
		s.close();
	}

}
