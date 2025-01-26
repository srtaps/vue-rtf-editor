<template>
  <div class="main-container">
    <div
      class="editor-container editor-container_document-editor"
      ref="editorContainerElement"
    >
      <div class="editor-container__menu-bar" ref="editorMenuBarElement"></div>
      <div class="editor-container__toolbar" ref="editorToolbarElement"></div>
      <div class="editor-container__editor-wrapper">
        <div class="editor-container__editor">
          <div ref="editorElement">
            <ckeditor
              v-if="editor && config"
              :editor="editor"
              :config="config"
              @ready="onReady"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, useTemplateRef } from "vue";
import { Ckeditor } from "@ckeditor/ckeditor5-vue";

import {
  DecoupledEditor,
  Alignment,
  AutoImage,
  AutoLink,
  Autosave,
  BlockQuote,
  Bold,
  Code,
  Essentials,
  GeneralHtmlSupport,
  Heading,
  HorizontalLine,
  ImageBlock,
  ImageInsert,
  ImageInsertViaUrl,
  ImageStyle,
  ImageToolbar,
  ImageUpload,
  Italic,
  Link,
  List,
  ListProperties,
  Paragraph,
  RemoveFormat,
  SimpleUploadAdapter,
  Strikethrough,
  Subscript,
  Superscript,
  Table,
  TableCellProperties,
  TableProperties,
  TableToolbar,
  Underline,
} from "ckeditor5";

import "ckeditor5/ckeditor5.css";

const emit = defineEmits(["editor-ready"]);

const LICENSE_KEY = "GPL"; // or <YOUR_LICENSE_KEY>.

const editorToolbar = useTemplateRef("editorToolbarElement");
const editorMenuBar = useTemplateRef("editorMenuBarElement");

const isLayoutReady = ref(false);

const editor = DecoupledEditor;

const config = computed(() => {
  if (!isLayoutReady.value) {
    return null;
  }

  return {
    toolbar: {
      items: [
        "heading",
        "|",
        "bold",
        "italic",
        "underline",
        "strikethrough",
        "subscript",
        "superscript",
        "code",
        "removeFormat",
        "|",
        "horizontalLine",
        "link",
        // "insertImage",
        // "insertImageViaUrl",
        "insertTable",
        "blockQuote",
        "|",
        "alignment",
        "|",
        "bulletedList",
        "numberedList",
      ],
      shouldNotGroupWhenFull: false,
    },
    plugins: [
      Alignment,
      AutoImage,
      AutoLink,
      Autosave,
      BlockQuote,
      Bold,
      Code,
      Essentials,
      GeneralHtmlSupport,
      Heading,
      HorizontalLine,
      // ImageBlock,
      // ImageInsert,
      // ImageInsertViaUrl,
      // ImageStyle,
      // ImageToolbar,
      // ImageUpload,
      Italic,
      Link,
      List,
      ListProperties,
      Paragraph,
      RemoveFormat,
      SimpleUploadAdapter,
      Strikethrough,
      Subscript,
      Superscript,
      Table,
      TableCellProperties,
      TableProperties,
      TableToolbar,
      Underline,
    ],
    heading: {
      options: [
        {
          model: "paragraph",
          title: "Paragraph",
          class: "ck-heading_paragraph",
        },
        {
          model: "heading1",
          view: "h1",
          title: "Heading 1",
          class: "ck-heading_heading1",
        },
        {
          model: "heading2",
          view: "h2",
          title: "Heading 2",
          class: "ck-heading_heading2",
        },
        {
          model: "heading3",
          view: "h3",
          title: "Heading 3",
          class: "ck-heading_heading3",
        },
        {
          model: "heading4",
          view: "h4",
          title: "Heading 4",
          class: "ck-heading_heading4",
        },
        {
          model: "heading5",
          view: "h5",
          title: "Heading 5",
          class: "ck-heading_heading5",
        },
        {
          model: "heading6",
          view: "h6",
          title: "Heading 6",
          class: "ck-heading_heading6",
        },
      ],
    },
    htmlSupport: {
      allow: [
        {
          name: /^.*$/,
          styles: true,
          attributes: true,
          classes: true,
        },
      ],
    },
    image: {
      toolbar: [
        "imageTextAlternative",
        "|",
        "imageStyle:alignBlockLeft",
        "imageStyle:block",
        "imageStyle:alignBlockRight",
      ],
      styles: {
        options: ["alignBlockLeft", "block", "alignBlockRight"],
      },
    },
    initialData: "",
    licenseKey: LICENSE_KEY,
    link: {
      addTargetToExternalLinks: true,
      defaultProtocol: "https://",
      decorators: {
        toggleDownloadable: {
          mode: "manual",
          label: "Downloadable",
          attributes: {
            download: "file",
          },
        },
      },
    },
    list: {
      properties: {
        styles: true,
        startIndex: true,
        reversed: true,
      },
    },
    menuBar: {
      isVisible: true,
    },
    placeholder: "Type or paste your content here!",
    table: {
      contentToolbar: [
        "tableColumn",
        "tableRow",
        "mergeTableCells",
        "tableProperties",
        "tableCellProperties",
      ],
    },
  };
});

const editorInstance = ref(null);

function getEditorContent() {
  return editorInstance.value.getData();
}

function setEditorContent(newContent) {
  editorInstance.value.setData(newContent);
}

onMounted(() => {
  isLayoutReady.value = true;
});

function onReady(editor) {
  editorInstance.value = editor;

  [...editorToolbar.value.children].forEach((child) => child.remove());
  [...editorMenuBar.value.children].forEach((child) => child.remove());

  editorToolbar.value.appendChild(editor.ui.view.toolbar.element);
  editorMenuBar.value.appendChild(editor.ui.view.menuBarView.element);

  emit("editor-ready");
}

defineExpose({
  getEditorContent,
  setEditorContent,
});
</script>
