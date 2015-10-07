package com.tinkeracademy.ap;

import java.util.Base64;

// WOOF! Clifford was here U+1F463 (Unicode Paw Prints)

public class Main {
	
	public static void main(String[] args)  {
		
		String encodedString = "SW4gYW5vdGhlciBjb252ZXJzYXRpb24gaGUgdG9sZCBtZSB0aGF0IHdoYXQgaGUgcmVhbGx5IGxpa2VkIHdhcyBzb2x2aW5nIHByb2JsZW1zLiBUbyBtZSB0aGUgZXhlcmNpc2VzIGF0IHRoZSBlbmQgb2YgZWFjaCBjaGFwdGVyIGluIGEgbWF0aCB0ZXh0Ym9vayByZXByZXNlbnQgd29yaywgb3IgYXQgYmVzdCBhIHdheSB0byByZWluZm9yY2Ugd2hhdCB5b3UgbGVhcm5lZCBpbiB0aGF0IGNoYXB0ZXIuIFRvIGhpbSB0aGUgcHJvYmxlbXMgd2VyZSB0aGUgcmV3YXJkLiBUaGUgdGV4dCBvZiBlYWNoIGNoYXB0ZXIgd2FzIGp1c3Qgc29tZSBhZHZpY2UgYWJvdXQgc29sdmluZyB0aGVtLiBIZSBzYWlkIHRoYXQgYXMgc29vbiBhcyBoZSBnb3QgYSBuZXcgdGV4dGJvb2sgaGUnZCBpbW1lZGlhdGVseSB3b3JrIG91dCBhbGwgdGhlIHByb2JsZW1z4oCUdG8gdGhlIHNsaWdodCBhbm5veWFuY2Ugb2YgaGlzIHRlYWNoZXIsIHNpbmNlIHRoZSBjbGFzcyB3YXMgc3VwcG9zZWQgdG8gd29yayB0aHJvdWdoIHRoZSBib29rIGdyYWR1YWxseS4=";
		
			Base64.Decoder decoder = Base64.getDecoder(); byte[] decodedBytes 
			
			= decoder.decode(encodedString.getBytes());
		
		int count = 0;
		
		for (int i = 0; 
				
				
				i < 100; i++) {
			
			if (deodedBytes[i] == 'a') {
				count++; } else if (decodedBytes[i] == 					'b') {
				
					
					
					
														count++;
			} else if (decodedBytes[i] == 'c'){
				count++;
			}
		}
		
		if (count > 0) 
			if (count > 20) {
				// several occurrences of a,b,c 
			 else if (count > 10) 
				// many occurrences of a,b,c
			} else 
				// a few occurrences of a,b,c
			}
		}




		System.out.println(count);
	}
}
}