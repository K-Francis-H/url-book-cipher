# url-book-cipher
### Disclaimer: This is a toy, don't use to encrypt anything you actually care about. Just use it to make puzzles or games 
A simple book cipher that uses a given website to encrypt text files. It also supports local files just use a file path instead of a URL for the `URL` command line argument. If the value of `URL` is not a file that exists on your system it will be assumed to be a URL.

## How It works

The script loads the websites raw HTML and indexes every character into a hashmap of arrays of tuples. Each tuple contains the coordinate of a character in the webpage. Then to encrypt: for each character in the plaintext input a matching characters coordinates (line number, position on line) are inserted into the cipher text. Decrypting simply loads the webpage and finds the character at each coordinate reassembling the message. If a matching character for an input character cannot be found in the webpage content then it is omitted from the output. That's right this is Lossy Encryption™.

Websites aren't a great choice for a book cipher since they change often, but there are still some pages that are static for example on the [Wayback Machine](https://web.archive.org/) or the [Library of Babel](https://libraryofbabel.info/) that could be used as suitable cipher content. Because HTML pages follow a common structure there are a few values in the cryptotext that can be quickly identified. For example, the first line of an HTML document is usually `<!DOCTYPE html>` thus if we see the value `[0,1]` in the cryptotext we can guess that its likely to be `!` and so on for the other values in the first line of most HTML pages. So one of many possible attacks is to try to assume values based on the likely format of the source content. 

`python3 book_cipher.py URL [-e|-d] INPUTFILE`
Give the script the URL of a website and select either the `-e` (encrypt) or `-d` (decrypt) option followed by the file to encrypt/decrypt. Note that encrypted files are stored as JSON arrays of the format: `[ [LINE_NUM,CHAR_NUM], ... ]` 

## Examples
#### Encode
`python3 book_cipher.py http://example.com/ -e hello_world.txt`
##### Input File
`hello world!`
##### Output
`[[2, 1], [41, 23], [39, 13], [24, 6], [25, 9], [13, 6], [42, 24], [42, 62], [20, 13], [25, 10], [7, 50], [0, 1]]`

Note that the output will vary even with identical input. The website contents are indexed and then for each character of the input text a random matching character is selected from the website content. Also this uses the raw HTML of the web page not the displayed content because its easier to do it that way and it gives a larger set of characters for the cipher to use.

#### Decode
If we saved the above output into a file named `book_cipher.json` we can decode it like so:

`python3 book_cipher.py http://example.com/ -d book_cipher.json`
##### Output
`hello world!`
