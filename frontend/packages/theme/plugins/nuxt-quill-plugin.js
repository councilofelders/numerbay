import Vue from 'vue';

import Quill from 'quill';
import VueQuillEditor from 'vue-quill-editor';

import MarkdownShortcuts from 'quill-markdown-shortcuts-for-vue-quill-editor';
Quill.register('modules/markdownShortcuts', MarkdownShortcuts);

Vue.use(VueQuillEditor);
