/*
 * jQuery UI Spinner @VERSION
 *
 * Copyright (c) 2008 jQuery
 * Dual licensed under the MIT (MIT-LICENSE.txt)
 * and GPL (GPL-LICENSE.txt) licenses.
 *
 * http://docs.jquery.com/UI/Spinner
 *
 * Depends:
 *  ui.core.js
 */
(function($) {

// shortcut constants
var hover = 'ui-state-hover',
	active = 'ui-state-active',
	namespace = '.spinner';

$.widget('ui.spinner', {
	_init: function() {
		var self = this,
			validChars;
					
		function parse(val, ifNull) {
			if (val == null)
				val = ifNull;
			if (typeof val == 'string')
				val = self._parseValue(val, self.options.radix, self.options.groupSeparator, self.options.radixPoint);
			return isNaN(val) ? null : val;
		}
	
		self._trigger('init', null, self.ui(null));
		
		// initialize variables
		// _curDelay can't be initialized as part of the prototype because all widgets would share the same object
		self._curDelay = {};
		self.focused = false;
		self.hovered = false;

		// perform data bind on generic objects
		if (self.options.items != null && typeof self.options.items[0] == 'object' && !self.element.is('input')) {
			var data = this.options.items;
			for (var i=0; i<data.length; i++) {
				self._addItem(data[i]);
			}
		}
		
		// Create list of valid characters used to build regexs
		validChars = '\\-\\' + self.options.radixPoint;
		if (self.options.groupSeparator)
			validChars += '\\' + self.options.groupSeparator;
		if (self.options.radix < 10)
			validChars += '0-' + self.options.radix;
		else {
			validChars += '0-9'
			if (self.options.radix > 10)
				validChars += 'a-' + String.fromCharCode('a'.charCodeAt(0) + self.options.radix - 11);
		}
		self.validChars = validChars;

		// Parse min, max, step, and pageStep for strings based on radix, apply HTML5 attributes if they are null
		self.options.min = parse(self.options.min, self.element.attr('min'));
		self.options.max = parse(self.options.max, self.element.attr('max'));
		self.options.step = parse(self.options.step, self.element.attr('step')) || 1;
		self.options.pageStep = parse(self.options.pageStep);
		
		// check for precision in steppinng and set _precision as internal
		self._precision = parseInt(self.options.precision, 10);
		if (self.options.step.toString().indexOf('.') != -1 && self._precision == 0) {
			var s = self.options.step.toString();
			self._precision = s.slice(s.indexOf('.')+1, s.length).length;
		}
				
		//Initialize needed constants
		self.element
			.addClass('ui-spinner-box')
			.attr('autocomplete', 'off'); // switch off autocomplete in opera
		
		// force a width if passed through options
		if (self.options.width) {
			self.element.width(self.options.width);
		}

		self._setValue( isNaN(self._getValue()) ? self.options.value : self._getValue() );
		
		var widget = self.element
		.wrap('<div>')
		.parent()
			.addClass('ui-spinner ui-widget ui-widget-content ui-corner-all ui-spinner-'+self.options.dir)
			// check for IE	
			.css({
				display: !$.support.opacity && $(self).css('display', 'inline-block') ? 'inline' : false
			})
			.append('<a class="ui-spinner-button ui-spinner-up ui-state-default ui-corner-t'+ self.options.dir.substr(-1,1) +'"><span class="ui-spinner-button-inner"><span class="ui-icon ui-icon-triangle-1-n">&#9650;</span></span></a>')
			.find('.ui-spinner-up')
				.bind('mousedown', function(event) {
					$(this).addClass(active);
					if (!self.counter) {
						self.counter = 1;
					}
					self._mousedown(100, '_up', event);
				})
				.bind('mouseup', function(event) {
					$(this).removeClass(active);
					if (self.counter == 1) {
						self._up(self.options.step, event);
					}
					self._mouseup(event);
				})
				// mousedown/mouseup capture first click, now handle second click
				.bind('dblclick', function(event) {
					if ($.browser.msie) {
						$(this).removeClass(active);
						self._up(self.options.step, event);
						self._mouseup(event);
					}
				})
			.end()
			.append('<a class="ui-spinner-button ui-spinner-down ui-state-default ui-corner-b'+ self.options.dir.substr(-1,1) +'"><span class="ui-spinner-button-inner"><span class="ui-icon ui-icon-triangle-1-s">&#9660;</span></span></a>')
			.find('.ui-spinner-down')
				.bind('mousedown', function(event) {
					$(this).addClass(active);
					if (!self.counter) {
						self.counter = 1;
					}
					self._mousedown(100, '_down', event);
				})				
				.bind('mouseup', function(event) {
					$(this).removeClass(active);
					if (self.counter == 1) {
						self._down(self.options.step, event);
					}
					self._mouseup(event);
				})
				// mousedown/mouseup capture first click, now handle second click in IE
				.bind('dblclick', function(event) {
					if ($.browser.msie) {
						$(this).removeClass(active);
						self._down(self.options.step, event);
						self._mouseup(event);
					}
				})
			.end()
			.hover(function() {
				self.hovered = true;
				if (typeof self.options.hide != 'boolean' && !self.focused && !self.disabled)
					self._delay(self._show, 100, 'hide', self.options.hide);
			}, function() {
				self.hovered = false;
				if (typeof self.options.hide != 'boolean' && !self.focused)
					self._delay(self._hide, 100, 'hide', self.options.hide);
			});
		
		self.buttons = widget.find('button')
			.hover(function() {
				$(this).addClass(hover);
			}, function(event) {
				$(this).removeClass(active + ' ' + hover);
				if (self.timer) {
					self._mouseup(event);
				}
			});
		if (self.options.hide)
			self._hide();

		// Give the spinner casing a unique id only if one exists in original input 
		// - this should aid targetted customisations if a page contains multiple instances
		self.element.attr('id', function(){
			if (this.id) {
				$(this).parent().attr('id', this.id+'-ui-spinner');
			}
		});

		// DataList: Set contraints for object length and step size. 
		// Manipulate height of spinner.
		self._items = self.element.children().length;
		if (self._items > 1) {
			var margins = self.element.outerHeight(true) - self.element.outerHeight();
			var height = self.element.outerHeight()/self._items + margins*2;
			//var height = self.options.height;
			self.element
			.addClass('ui-spinner-list')
			.height(height)
			.children()
				.addClass('ui-spinner-listitem')
				.height(height)
				.css('overflow', 'hidden')
			.end()
			.parent()
				.height(height)
			.end();
			self.options.step = 1;
			self.options.min = 0;
			self.options.max = self._items-1;
		}

		self.element
		.bind('keydown'+namespace, function(event) {
			if (!self.counter) {
				self.counter = 1;
			}
			return self._keydown.call(self, event);
		})
		.bind('keyup'+namespace, function(event) {
			self.counter = 0;
			self._trigger('change', event, self.ui());
		})
		.bind('focus'+namespace, function() {
			self.focused = true;
			if (!self.hovered && typeof self.options.hide != 'boolean' && !self.disabled)
				self._delay(self._show, 100, 'hide', self.options.hide);
		})
		.bind('blur'+namespace, function(event) {
			self.focused = false;
			if (!self.hovered && typeof self.options.hide != 'boolean')
				self._delay(self._hide, 100, 'hide', self.options.hide);
			self._cleanUp();
		});

		if ($.fn.mousewheel && self.options.mouseWheel) {
			self.element.mousewheel(self._mousewheel);
		}
		
		// disable spinner if element was already disabled
		if (self.element.attr("disabled"))
			self.disable();
			
		//self._extend('initComplete');
	},

	_constrain: function() {
		if (this.options.min != null && this._getValue() < this.options.min) {
			this._setValue(this.options.min);
		}
		if (this.options.max != null && this._getValue() > this.options.max) {
			this._setValue(this.options.max);
		}
	},
	_cleanUp: function() {
		this._setValue(this._getValue());
		this._constrain();
	},
	_spin: function(d, step, event) {
		if (this.disabled) {
			return;
		}
		this._trigger('start', event, this.ui());
		
		var value = this._getValue();

		if (isNaN(value)) {
			value = this.options.value;
		}
		this._setValue(value + (d == 'up' ? 1:-1) *(this.options.incremental && this.counter > 100 ? (this.counter > 200 ? 100 : 10) : 1) * step);
		this._animate(d);
		this._constrain();
		if (this.counter) {
			this.counter++;
		}
		
		this._trigger('spin', event, this.ui());
		this._trigger('stop', event, this.ui());
	},
	_down: function(step, event) {
		this._spin('down', step, event);
	},
	_up: function(step, event) {
		this._spin('up', step, event);
	},
	_mousedown: function(i, d, event) {
		var self = this;
		i = i || 100;
		if (this.timer) {
			window.clearInterval(this.timer);
			this.timer = 0;
		}
		this.timer = window.setInterval(function() {
			self[d](self.options.step, event);
			if (self.options.incremental && self.counter > 20) {
				self._mousedown(20, d, event);
			}
		}, i);
	},
	_mouseup: function(event) {
		this.counter = 0;
		if (this.timer) {
			window.clearInterval(this.timer);
			this.timer = 0;
		}
		this.element[0].focus();
		this._trigger('change', event, this.ui());
	},
	_keydown: function(event) {
		var KEYS = $.ui.keyCode;

		if (event.keyCode == KEYS.UP) {
			this._up(this.options[event.shiftKey ? 'pageStep' : 'step'], event);
		}
		if (event.keyCode == KEYS.DOWN) {
			this._down(this.options[event.shiftKey ? 'pageStep' : 'step'], event);
		}
		if (event.keyCode == KEYS.PAGE_UP) {
			this._up(this.options.pageStep, event);
		}
		if (event.keyCode == KEYS.PAGE_DOWN) {
			this._down(this.options.pageStep, event);
		}
		if (event.keyCode == KEYS.HOME) {
			//Home key goes to min, if defined, else to options.value
			this._setValue(this.options.min || this.options.value);
		}
		if (event.keyCode == KEYS.END && this.options.max != null) {
			//End key goes to maximum
			this._setValue(this.options.max);
		}
		return (event.keyCode == KEYS.TAB || event.keyCode == KEYS.BACKSPACE ||
			event.keyCode == KEYS.LEFT || event.keyCode == KEYS.RIGHT || event.keyCode == KEYS.PERIOD || 
			event.keyCode == KEYS.NUMPAD_DECIMAL || event.keyCode == KEYS.NUMPAD_SUBTRACT || 
			(event.keyCode >= 96 && event.keyCode <= 105) || // add support for numeric keypad 0-9
			(new RegExp('[' + this.validChars + ']', 'i').test(String.fromCharCode(event.keyCode)))) ? true : false;
	},
	_mousewheel: function(event, delta) {
		// this = element, not widget, in event call
		// we must use a function that is a member of the widget for binding/unbinding the event on option changes
		var self = $.data(this, 'spinner');
		
		delta = ($.browser.opera ? -delta / Math.abs(delta) : delta);
		self[delta > 0 ? '_up' : '_down'](self.options.step, event);
		if (self.timeout) {
			window.clearTimeout(self.timeout);
			self.timeout = 0;
		}
		self.timeout = window.setTimeout(function(){self._trigger('change', event, self.ui());}, 400);
		event.preventDefault();
	},
	_parseValue: function(val, radix, groupSeparator, radixPoint) {
		// Because groupSeparator is included in the regex, we must replace it independently
		if (groupSeparator)
			val = val.replace(groupSeparator, '');
			
		val = val.replace(new RegExp('[^' + this.validChars + ']', 'gi'), '').split(radixPoint);
		
		result = parseInt(val[0], radix);
		if (val.length > 1)
			result += parseInt(val[1], radix) / Math.pow(radix, val[1].length) *
				// must test first character of val[0] for minus sign because -0 is parsed as 0 in result
				(val[0][0] == '-' ? -1 : 1);
		
		return result;
	},
	_getValue: function() {
		return this._parseValue(this.element.val(), this.options.radix, this.options.groupSeparator, this.options.radixPoint);
	},
	_setValue: function(newVal) {
		if (isNaN(newVal)) {
			newVal = this.options.value;
		}
		this.element.val(
			this.options.currency ? 
				$.ui.spinner.format.currency(newVal, this.options.currency, this.options.groupSeparator, this.options.radixPoint) : 
				$.ui.spinner.format.number(newVal, this._precision, this.options.radix, this.options.groupSeparator, this.options.radixPoint, this.options.padLength)
		);
	},
	_animate: function(d) {
		if (this.element.hasClass('ui-spinner-list') && ((d == 'up' && this._getValue() <= this.options.max) || (d == 'down' && this._getValue() >= this.options.min)) ) {
			this.element.animate({marginTop: '-' + this._getValue() * this.element.parent().height() }, {
				duration: 'fast',
				queue: false
			});
		}
	},
	_addItem: function(obj, fmt) {
		if (!this.element.is('input')) {
			var wrapper = 'div';
			if (this.element.is('ol') || this.element.is('ul')) {
				wrapper = 'li';
			}
			var html = obj; // string or object set it to html first

			if (typeof obj == 'object') {
				var format = (fmt !== undefined ? fmt : this.options.format);

				html = format.replace(/%(\(([^)]+)\))?/g, 
					(function(data){
						return function(match, a, lbl) { 
							if (!lbl) {
								for (var itm in data) {
									return data[itm]; // return the first item only
								}
							} else {
								return data[lbl];
							}
						};
					})(obj)
				);
			}
			this.element.append('<'+ wrapper +' class="ui-spinner-dyn">'+ html + '</'+ wrapper +'>');
		}
	},
	// delays a function call, allowing only one at a time of the same type
	_delay: function(callback, delay, type) {
		type = type || 'a';

		var self = this,
			curDelay = self._curDelay[type] || {},
			args = Array.prototype.slice.call(arguments, 3);
		
		// reassign in case it's a new delay
		self._curDelay[type] = curDelay; 
		
		if (curDelay.i) {
			// don't do anything if resetting the same delay
			if (curDelay.f === callback) return;
			clearTimeout(curDelay.i);
		}
		
		curDelay.f = callback;
		curDelay.i = setTimeout(function() {
			curDelay.i = 0;
			curDelay.f.apply(self, args);
		}, delay);
	},
	_show: function(speed) {
		var buttons = this.buttons.stop();
		if (!speed)
			buttons.css('opacity', 1);
		else
			buttons.fadeTo(speed, 1);
		return this;
	},
	_hide: function(speed) {
		// also removeClass(hover) in case it was left despite losing mouse hover
		var buttons = this.buttons.stop().removeClass(hover);
		if (!speed)
			buttons.css('opacity', 0);
		else
			buttons.fadeTo(speed, 0);
		return this;
	},
	_setData: function(key, value) {
		if ((key == 'mouseWheel') && (value != this.options.mouseWheel) && $.fn.mousewheel)
			this.element[value ? 'mousewheel' : 'unmousewheel'](this._mousewheel);
		else if (key == 'hide') {
			if (typeof value != 'boolean')
				this[this.hovered || this.focused ? '_show' : '_hide']();
			else if (value)
				this._hide();
			else
				this._show();
		}
		
		$.widget.prototype._setData.call(this, key, value);
	},
	
	plugins: {},
	ui: function(event) {
		return {
			options: this.options,
			element: this.element,
			value: this._getValue(),
			add: this._addItem
		};
	},
	destroy: function() {
		if (!$.data(this.element[0], 'spinner')) {
			return;
		}
		if ($.fn.mousewheel) {
			this.element.unmousewheel();
		}
		this.element
			.removeClass('ui-spinner-box ui-spinner-list')
			.removeAttr('disabled')
			.removeAttr('autocomplete')
			.removeData('spinner')
			.unbind(namespace)
			.siblings()
				.remove()
			.end()
			.children()
				.removeClass('ui-spinner-listitem')
				.remove('.ui-spinner-dyn')
			.end()
			.parent()
				.removeClass('ui-spinner ui-state-disabled')
				.before(this.element.clone())
				.remove()
			.end();
	},
	enable: function() {
		this.element
			.removeAttr('disabled')
			.siblings()
				.removeAttr('disabled')
			.parent()
				.removeClass('ui-state-disabled');
		this.disabled = false;
		return this;
	},
	disable: function() {
		this.element
			.attr('disabled', true)
			.siblings()
				.attr('disabled', true)
			.parent()
				.addClass('ui-state-disabled');
		this.disabled = true;
		return this;
	},
	value: function(newVal) {
		if (!arguments.length)
			return this._getValue();
			
		this._setValue(newVal);
		return this;
	}
});

$.extend($.ui.spinner, {
	version: "@VERSION",
	eventPrefix: "spin",
	defaults: {
		precision: 0,
		radix: 10,
		padLength: 0,
		max: null,
		min: null,
		
		// null defaults to 1 in _init.  We use null so that we can detect if passed value should override HTML5 attribute
		step: null,
		pageStep: 5,
		value: 0,

		incremental: true,
		mouseWheel: true,
		currency: false,
		
		format: '%',
		groupSeparator: '',
		radixPoint: '.',
		
		items: null,
		width: false,
		hide: false,
		
		dir: 'ltr'
	},
	format: {
		currency: function(num, sym, group, pt) {
			num = isNaN(num) ? 0 : num;
			return (num !== Math.abs(num) ? '-' : '') + sym + this.number(Math.abs(num), 2, 10, group || ',', pt);
		},
		number: function(num, dec, radix, group, pt, padLength) {
			var whole = Math.floor(Math.abs(num)),
				result = whole.toString(radix),
				part = Math.floor(((Math.abs(num) - whole) * Math.pow(radix, dec))).toString(radix),
				regex = /(\d+)(\d{3})/;
			
			while (regex.test(result) && group) result=result.replace(regex, '$1'+group+'$2');
			
			if (dec > 0) {
				while (part.length < dec) part = '0' + part;
				result += pt + part;
			}
			
			while (padLength && (result.length < padLength))
				result = '0' + result;
						
			return (num < 0 ? '-' : '') + result;
		}
	}
});

})(jQuery);
