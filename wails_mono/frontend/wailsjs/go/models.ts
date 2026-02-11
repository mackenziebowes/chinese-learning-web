export namespace models {
	
	export class Entry {
	    chinese: string;
	    pinyin: string;
	    english: string;
	
	    static createFrom(source: any = {}) {
	        return new Entry(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.chinese = source["chinese"];
	        this.pinyin = source["pinyin"];
	        this.english = source["english"];
	    }
	}

}

