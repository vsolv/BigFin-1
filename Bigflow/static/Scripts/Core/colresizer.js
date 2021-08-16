angular.module("rzTable", []);

angular.module("rzTable").directive('rzTable', ['resizeStorage', '$injector', '$parse', function(resizeStorage, $injector, $parse) {

    var mode;
    var saveTableSizes;
    var profile;

    var columns = null;
    var ctrlColumns = null;
    var handleColumns = null;
    var listener = null;
    var handles = []
    var table = null;
    var container = null;
    var resizer = null;
    var isFirstDrag = true;

    var cache = null;

    RzController.$inject = ['$scope', '$attrs', '$element'];

    function RzController($scope) {

    }

    function link(scope, element, attr) {
        // Set global reference to table
        table = element;

        // Set global reference to container
        container = scope.container ? angular.element(scope.container) : angular.element(table).parent();

        // Set options to an empty object if undefined
        scope.options = attr.rzOptions ? scope.options || {} : {}

        // Add css styling/properties to table
        angular.element(table).addClass(scope.options.tableClass || 'rz-table');

        // Initialise handlers, bindings and modes
        initialiseAll(table, attr, scope);

        // Bind utility functions to scope object
        bindUtilityFunctions(table, attr, scope)

        // Watch for changes in columns
        watchTableChanges(table, attr, scope)

        // Watch for scope bindings
        setUpWatchers(table, attr, scope)
    }

    function renderWatch(table, attr, scope) {
      return function(oldVal, newVal) {
        if (newVal !== oldVal) {
          cleanUpAll(table);
          initialiseAll(table, attr, scope);
        }
      }
    }

    function setUpWatchers(table, attr, scope) {
        scope.$watch('profile', renderWatch(table, attr, scope))
        scope.$watch('mode', renderWatch(table, attr, scope))
    }

    function watchTableChanges(table, attr, scope) {
        scope.$watch(function () {
          return angular.element(table).find('th').length;
        }, renderWatch(table, attr, scope));
    }

    function bindUtilityFunctions(table, attr, scope) {
        if (!attr.rzModel) return;
        var model = $parse(attr.rzModel)
        model.assign(scope.$parent, {
            update: function() {
                cleanUpAll(table)
                initialiseAll(table, attr, scope)
            },
            reset: function() {
                resetTable(table)
                this.clearStorageActive()
                this.update()
            },
            clearStorage: function() {
                resizeStorage.clearAll()
            },
            clearStorageActive: function() {
                resizeStorage.clearCurrent(table, mode, profile)
            }
        })
    }

    function cleanUpAll(table) {
        isFirstDrag = true;
        deleteHandles(table);
    }

    function resetTable(table) {
        angular.element(table).outerWidth('100%');
        angular.element(table).find('th').width('auto');
    }

    function deleteHandles(table) {
        handles.map(function(h) { h.remove() })
        handles = []
    }

    function initialiseAll(table, attr, scope) {
        // Get all column headers
        columns = angular.element(table).find('th');

        mode = scope.mode;
        saveTableSizes = angular.isDefined(scope.saveTableSizes) ? scope.saveTableSizes : true;
        profile = scope.profile

        // Get the resizer object for the current mode
        var ResizeModel = getResizer(scope, attr);
        if (!ResizeModel) return;
        resizer = new ResizeModel(table, columns, container);

        if (saveTableSizes) {
            // Load column sizes from saved storage
            cache = resizeStorage.loadTableSizes(table, scope.mode, scope.profile)
        }

        // Decide which columns should have a handler attached
        handleColumns = resizer.handles(columns);

        // Decide which columns are controlled and resized
        ctrlColumns = resizer.ctrlColumns;

        // Execute setup function for the given resizer mode
        resizer.setup();

        // Set column sizes from cache
        setColumnSizes(cache);

        // Initialise all handlers for every column
        angular.forEach(handleColumns,function(column) {
            initHandle(scope, table, column);
        })

    }

    function initHandle(scope, table, column) {
        // Prepend a new handle div to the column

        var handle = angular.element('<div>');
        
        handle.addClass(scope.options.handleClass || 'rz-handle');
        
        angular.element(column).prepend(handle);

        // Add handles to handles for later removal
        handles.push(handle)

        // Use the middleware to decide which columns this handle controls
        var controlledColumn = resizer.handleMiddleware(handle, column)

        // Bind mousedown, mousemove & mouseup events
        bindEventToHandle(scope, table, handle, controlledColumn);
    }

    function bindEventToHandle(scope, table, handle, column) {

        // This event starts the dragging
        angular.element(handle).bind('mousedown',  function(event) {
            if (isFirstDrag) {
                resizer.onFirstDrag(column, handle);
                resizer.onTableReady();
                isFirstDrag = false;
            }

            scope.options.onResizeStarted && scope.options.onResizeStarted(column)

            var optional = {}
            if (resizer.intervene) {
                optional = resizer.intervene.selector(column);
                optional.column = optional;
                optional.orgWidth = angular.element(optional).width();
            }

            // Prevent text-selection, object dragging ect.
            event.preventDefault();

            // Change css styles for the handle
            angular.element(handle).addClass(scope.options.handleClassActive || 'rz-handle-active');

            // Get mouse and column origin measurements
            var orgX = event.clientX;
            var orgWidth = angular.element(column).width();

            // On every mouse move, calculate the new width
            listener = calculateWidthEvent(scope, column, orgX, orgWidth, optional)
            angular.element(window).mousemove(listener)

            // Stop dragging as soon as the mouse is released
            angular.element(window).one('mouseup', unbindEvent(scope, column, handle))
        })
    }

    function calculateWidthEvent(scope, column, orgX, orgWidth, optional) {
        return function(event) {
            // Get current mouse position
            var newX = event.clientX;

            // Use calculator function to calculate new width
            var diffX = newX - orgX;
            var newWidth = resizer.calculate(orgWidth, diffX);

            if (newWidth < getMinWidth(column)) return;
            if (resizer.restrict(newWidth, diffX)) return;

            // Extra optional column
            if (resizer.intervene){
                var optWidth = resizer.intervene.calculator(optional.orgWidth, diffX);
                if (optWidth < getMinWidth(optional.column)) return;
                if (resizer.intervene.restrict(optWidth, diffX)) return;
                angular.element(optional.column).width(optWidth)
            }

            scope.options.onResizeInProgress && scope.options.onResizeInProgress(column, newWidth, diffX)

            // Set size
            angular.element(column).width(newWidth);
        }
    }

    function getMinWidth(column) {
        // "25px" -> 25
        return parseInt(angular.element(column).css('min-width')) || 0;
    }

    function getResizer(scope, attr) {
        try {
            var mode = attr.rzMode ? scope.mode : 'BasicResizer';
            var Resizer = $injector.get(mode)
            return Resizer;
        } catch (e) {
            console.error("The resizer "+ scope.mode +" was not found");
            return null;
        }
    }


    function unbindEvent(scope, column, handle) {
        // Event called at end of drag
        return function( /*event*/ ) {
            angular.element(handle).removeClass(scope.options.handleClassActive || 'rz-handle-active');

            if (listener) {
                angular.element(window).unbind('mousemove', listener);
            }

            scope.options.onResizeEnded && scope.options.onResizeEnded(column)

            resizer.onEndDrag();

            saveColumnSizes();
        }
    }

    function saveColumnSizes() {
        if (!saveTableSizes) return;

        if (!cache) cache = {};
        angular.forEach(columns, function(column) {
            var colScope = angular.element(column).scope()
            var id = colScope.rzCol || angular.element(column).attr('id')
            if (!id) return;
            cache[id] = resizer.saveAttr(column);
        })

        resizeStorage.saveTableSizes(table, mode, profile, cache);
    }

    function setColumnSizes(cache) {
        if (!cache) {
            return;
        }

        angular.element(table).width('auto');
        
        angular.forEach(ctrlColumns,function( column){
            var colScope = angular.element(column).scope()
            var id = colScope.rzCol || angular.element(column).attr('id')
            var cacheWidth = cache[id];
            angular.element(column).css({ width: cacheWidth });
        })

        resizer.onTableReady();
    }

    // Return this directive as a object literal
    return {
        restrict: 'A',
        link: link,
        controller: RzController,
        scope: {
            mode: '=rzMode',
            profile: '=?rzProfile',
            // whether to save table sizes; default true
            saveTableSizes: '=?rzSave',
            options: '=?rzOptions',
            model: '=rzModel',
            container: '@rzContainer'
        }
    };

}]);

angular.module("rzTable").directive('rzCol', [function() {
  // Return this directive as a object literal
  return {
    restrict: 'A',
    priority: 650, /* before ng-if */
    link: link,
    require: '^^rzTable',
    scope: true
  };

  function link(scope, element, attr) {
    scope.rzCol = scope.$eval(attr.rzCol)
  }
}])
angular.module("rzTable").service('resizeStorage', ['$window', function($window) {

    var prefix = "ngColumnResize";

    this.loadTableSizes = function(table, mode, profile) {
        var key = getStorageKey(table, mode, profile);
        var object = $window.localStorage.getItem(key);
        return JSON.parse(object);
    }

    this.saveTableSizes = function(table, mode, profile, sizes) {
        var key = getStorageKey(table, mode, profile);
        if (!key) return;
        var string = JSON.stringify(sizes);
        $window.localStorage.setItem(key, string)
    }

    this.clearAll = function() {
        var keys = []
        for (var i = 0; i < $window.localStorage.length; ++i) {
            var key = localStorage.key(i)
            if (key && key.startsWith(prefix)) {
                keys.push(key)
            }
        }
        keys.map(function(k) { $window.localStorage.removeItem(k) })
    }

    this.clearCurrent = function(table, mode, profile) {
        var key = getStorageKey(table, mode, profile);
        if (key) {
            $window.localStorage.removeItem(key)
        }
    }

    function getStorageKey(table, mode, profile) {
        var id = table.attr('id');
        if (!id) {
            console.error("Table has no id", table);
            return undefined;
        }
        return prefix + '.' + table.attr('id') + '.' + mode + (profile ? '.' + profile : '');
    }

}]);

angular.module("rzTable").factory("ResizerModel", [function() {

    function ResizerModel(table, columns, container){
        this.table = table;
        this.columns = columns;
        this.container = container;

        this.handleColumns = this.handles();
        this.ctrlColumns = this.ctrlColumns();
    }

    ResizerModel.prototype.setup = function() {
        // Hide overflow by default
        angular.element(this.container).css({
            overflowX: 'hidden'
        })
    }

    ResizerModel.prototype.onTableReady = function () {
        // Table is by default 100% width
        angular.element(this.table).outerWidth('100%');
    };

    ResizerModel.prototype.getMinWidth = function(column) {
        // "25px" -> 25
        return parseInt(angular.element(column).css('min-width')) || 0;
    }

    ResizerModel.prototype.handles = function () {
        // By default all columns should be assigned a handle
        return this.columns;
    };

    ResizerModel.prototype.ctrlColumns = function () {
        // By default all columns assigned a handle are resized
        return this.handleColumns;
    };

    ResizerModel.prototype.onFirstDrag = function () {
        // By default, set all columns to absolute widths
        angular.forEach(this.ctrlColumns,function(column) {
          angular.element(column).css('width', angular.element(column)[0].getBoundingClientRect().width + 'px');
            //$(column).width($(column).width());
        })
    };

    ResizerModel.prototype.handleMiddleware = function (handle, column) {
        // By default, every handle controls the column it is placed in
        return column;
    };

    ResizerModel.prototype.restrict = function (newWidth) {
        return false;
    };

    ResizerModel.prototype.calculate = function (orgWidth, diffX) {
        // By default, simply add the width difference to the original
        return orgWidth + diffX;
    };

    ResizerModel.prototype.onEndDrag = function () {
        // By default, do nothing when dragging a column ends
        return;
    };

    ResizerModel.prototype.saveAttr = function (column) {
        return angular.element(column).outerWidth();
    };

    return ResizerModel;
}]);

/*angular.module("rzTable").factory("BasicResizer", ["ResizerModel", function(ResizerModel) {

    function BasicResizer(table, columns, container) {
        // Call super constructor
        ResizerModel.call(this, table, columns, container)

        // All columns are controlled in basic mode
        this.ctrlColumns = this.columns;

        this.intervene = {
            selector: interveneSelector,
            calculator: interveneCalculator,
            restrict: interveneRestrict
        }
    }

    // Inherit by prototypal inheritance
    BasicResizer.prototype = Object.create(ResizerModel.prototype);

    function interveneSelector(column) {
        return angular.element(column).next()
    }

    function interveneCalculator(orgWidth, diffX) {
        return orgWidth - diffX;
    }

    function interveneRestrict(newWidth){
        return newWidth < 25;
    }

    BasicResizer.prototype.setup = function() {
        // Hide overflow in mode fixed
        angular.element(this.container).css({
            overflowX: 'hidden'
        })

        angular.element(this.table).css({
            width: '100%'
        })
    };

    BasicResizer.prototype.handles = function() {
        // Mode fixed does not require handler on last column
        return angular.element(this.columns).not(':last')
    };

    BasicResizer.prototype.onFirstDrag = function() {
        // Replace all column's width with absolute measurements
        this.onEndDrag()
    };

    BasicResizer.prototype.onEndDrag = function () {
        // Calculates the percent width of each column
        var totWidth = angular.element(this.table).outerWidth();

        var callbacks = []

        // Calculate the width of every column
        angular.element(this.columns).each(function(index, column) {
            var colWidth = angular.element(column).outerWidth();
            var percentWidth = colWidth / totWidth * 100 + '%';
            callbacks.push(function() {
              angular.element(column).css({ width: percentWidth });
            })
        })

        // Apply the calculated width of every column
        callbacks.map(function(cb) { cb() })
    };

    BasicResizer.prototype.saveAttr = function (column) {
        return angular.element(column)[0].style.width;
    };

    // Return constructor
    return BasicResizer;

}]);

angular.module("rzTable").factory("FixedResizer", ["ResizerModel", function(ResizerModel) {

    function FixedResizer(table, columns, container) {
        // Call super constructor
        ResizerModel.call(this, table, columns, container)

        this.fixedColumn = angular.element(table).find('th').first();
        this.bound = false;
    }

    // Inherit by prototypal inheritance
    FixedResizer.prototype = Object.create(ResizerModel.prototype);

    FixedResizer.prototype.setup = function() {
        // Hide overflow in mode fixed
        angular.element(this.container).css({
            overflowX: 'hidden'
        })

        angular.element(this.table).css({
            width: '100%'
        })

        // First column is auto to compensate for 100% table width
        angular.element(this.columns).first().css({
            width: 'auto'
        });
    };

    FixedResizer.prototype.handles = function() {
        // Mode fixed does not require handler on last column
        return angular.element(this.columns).not(':last')
    };

    FixedResizer.prototype.ctrlColumns = function() {
        // In mode fixed, all but the first column should be resized
        return angular.element(this.columns).not(':first');
    };

    FixedResizer.prototype.onFirstDrag = function() {
        // Replace each column's width with absolute measurements
        angular.element(this.ctrlColumns).each(function(index, column) {
            angular.element(column).width(angular.element(column).width());
        })
    };

    FixedResizer.prototype.handleMiddleware = function (handle, column) {
        // Fixed mode handles always controll next neightbour column
        return angular.element(column).next();
    };

    FixedResizer.prototype.restrict = function (newWidth, diffX) {
        if (this.bound && this.bound < diffX) {
          this.bound = false
          return false
        } if (this.bound && this.bound > diffX) {
          return true
        } else if (this.fixedColumn.width() <= this.getMinWidth(this.fixedColumn)) {
            this.bound = diffX
            angular.element(this.fixedColumn).width(this.minWidth);
            return true;
        }
    };

    FixedResizer.prototype.onEndDrag = function () {
        this.bound = false
    };

    FixedResizer.prototype.calculate = function (orgWidth, diffX) {
        // Subtract difference - neightbour grows
        return orgWidth - diffX;
    };

    // Return constructor
    return FixedResizer;

}]);*/

angular.module("rzTable").factory("OverflowResizer", ["ResizerModel", function(ResizerModel) {

    function OverflowResizer(table, columns, container) {
        // Call super constructor
        ResizerModel.call(this, table, columns, container)
    }

    // Inherit by prototypal inheritance
    OverflowResizer.prototype = Object.create(ResizerModel.prototype);


    OverflowResizer.prototype.setup = function() {
        // Allow overflow in this mode
        angular.element(this.container).css({
            overflow: 'auto'
        });
    };

    OverflowResizer.prototype.onTableReady = function() {
        // For mode overflow, make table as small as possible
        angular.element(this.table).width(1);
    };

    // Return constructor
    return OverflowResizer;

}]);