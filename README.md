# USA Cycling Database Tools
Tools for working with the USA Cycling member "database" (CSV files *cough cough*) in Python. In other words, some help for the programming-inclined USA Cycling promoter.

The current focus is on getting data from the CSV files into a more useful format (no, copying and pasting into Excel is not actually more useful).

## Features
Load all data from USA Cycling's `wp_all_clubs2.csv1` and `wp_p_uscf_tn.csv` promoter files into Redis.

### Redis
Redis is a high-performance key-value store. Import to Redis for very fast web application lookups (i.e., text-field autocomplete) or statistical analysis.

### MySQL/Postgres/[otherRDBMS]
Import to a traditional relational database if you'd like. Models are fully foreign-keyed (caveat: riders with a club that doesn't exist in the clubs list being used will have their clubs unset).

## Bugs
Something's probably broken somewhere. Surprise? Use the GitHub issue tracker to notify me of bugs.

## Author
I'm Jacob Okamoto. I race bikes for the University of Minnesota. I also help run races. And code. Add those three things together and you get this.

## LICENSE

    Copyright (c) 2013, Jacob Okamoto
    All rights reserved.
    
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
        * Redistributions of source code must retain the above copyright
          notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright
          notice, this list of conditions and the following disclaimer in the
          documentation and/or other materials provided with the distribution.
        * Neither the name of the project nor the names of its contributors may be
          used to endorse or promote products derived from this software without
          specific prior written permission.
    
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
