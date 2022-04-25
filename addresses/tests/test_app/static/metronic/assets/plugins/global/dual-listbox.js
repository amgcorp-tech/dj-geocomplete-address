'use strict';

// Class definition
var KTDualListbox = function() {

  // Private functions
  var initDualListbox = function() {
    // Dual Listbox
    var listBoxes = $('.dual-listbox');

    listBoxes.each(function() {
      var $this = $(this);
      // get titles
      var availableTitle = ($this.attr('data-available-title') != null) ? $this.attr('data-available-title') : gettext('Available Options');
      var selectedTitle = ($this.attr('data-selected-title') != null) ? $this.attr('data-selected-title') : gettext('Selected Options');

      // get button labels
      var addLabel = ($this.attr('data-add') != null) ? $this.attr('data-add') : gettext('Add');
      var removeLabel = ($this.attr('data-remove') != null) ? $this.attr('data-remove') : gettext('Remove');
      var addAllLabel = ($this.attr('data-add-all') != null) ? $this.attr('data-add-all') : gettext('Add All');
      var removeAllLabel = ($this.attr('data-remove-all') != null) ? $this.attr('data-remove-all') : gettext('Remove All');

      // get options
      var options = [];
      // removed to fix duplicate bug
      // $this.children('option').each(function(i) {
      //   var value = $(this).val();
      //   var label = $(this).text();
      //   // options.push({text: label, value: value});
      // });

      // get search option
      var search = ($this.attr('data-search') != null) ? $this.attr('data-search') : '';

      // init dual listbox
      var dualListBox = new DualListbox($this.get(0), {
        addEvent: function(value) {
          //console.log(value);
        },
        removeEvent: function(value) {
          //console.log(value);
        },
        availableTitle: availableTitle,
        selectedTitle: selectedTitle,
        addButtonText: addLabel,
        removeButtonText: removeLabel,
        addAllButtonText: addAllLabel,
        removeAllButtonText: removeAllLabel,
        options: options,
      });

      if (search === 'false') {
        dualListBox.search.classList.add('dual-listbox__search--hidden');
      }

      // included needed classes for styling
      dualListBox.availableList.closest('div').classList += "col-lg-5 available-container";
      dualListBox.selectedList.closest('div').classList += "col-lg-5 selected-container";
      dualListBox.buttons.classList.add("text-center");
      window.dualListBox = dualListBox;
    });
  };

  return {
    // public functions
    init: function() {
      initDualListbox();
    },
  };
}();

KTUtil.onDOMContentLoaded(function() {
  KTDualListbox.init();
});

