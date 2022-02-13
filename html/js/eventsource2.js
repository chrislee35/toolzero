function EventSource2(url) {
    this.url = url;
    this.es = null;
    this.listeners = {};
}

EventSource2.prototype = {
    constructor: EventSource2,

    connect: function() {
        console.log("SSE Connecting to "+this.url)
        this.es = new EventSource(this.url);
        this.bindEvents();
    },

    disconnect: function() {
      console.log("SSE Disconnecting")
        if(this.es) {
          this.es.close();
          this.es = null;
        }
    },

    bindEvents: function() {
        for ( var type in this.listeners ) {
            var evs = this.listeners[type];
            for( var i = 0; i < evs.length; ++i ) {
                this.es.addEventListener( type, evs[i], false );
            }
        }
    },

    addEventListener: function( type, fn ) {
        if( !this.listeners[type] ) {
            this.listeners[type] = [];
        }

        this.listeners[type].push( fn );
        if( this.es ) {
            this.bindEvents();
        }
    }
}
