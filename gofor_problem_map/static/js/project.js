/* Project specific Javascript goes here. */

// Makes all textareas responsive to input
$('textarea').each(function () {
  this.setAttribute('rows', 1);
  this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
}).on('input', function () {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
});
