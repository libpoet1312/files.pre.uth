#include <stdio.h>
#include <stdlib.h>

#include "type_t.h"
#include "dlist.h"

dlist_t* create_dlist(comparator_t cmp, printer_t printer) {
  dlist_t* list = (dlist_t*) malloc(sizeof(dlist_t));
  if (!list) {
    exit(-1);
  }
  list->head = list->tail = NULL;
  list->size = 0;

  list->cmp = student_cmp;
  list->printer = student_print;

  return list;
}

void clear_dlist(dlist_t* list) {
  dnode_t* tmp_node;
  dnode_t* curr;
  //diatrexw tin lista kai diagrafw kathe stoixio tis
  curr = list->head;
  while (curr!=NULL) {
    tmp_node = curr;
    curr = curr->next;
    free(tmp_node); //diagrafi tou node
  }


}

void destroy_dlist(dlist_t* list) {
  clear_dlist(list);
  free(list);
}

int size(dlist_t* list) {
  return list->size;
}

bool insert(dlist_t* list, int index, type_t data) {
  int i;
  dnode_t* tmp_node;
  dnode_t* new_node;

  //elegxos oriwn
  if (index<0 || index>list->size) {
    return false;
  }

  if ((list->head == NULL) && (index != 0)){
        printf("%d Empty list \n", index);
        return false;
  }

  //dimioyrgia neou komvou
  new_node = (dnode_t*)malloc(sizeof(dnode_t));
  //tmp_node = (dnode_t*)malloc(sizeof(dnode_t));
  if (!new_node) {
    exit(-1);
  }
  new_node->data = data;


  if (index == 0){
    if (list->head == NULL) {
      // 1. enthesi stin arxi tis KENIS listas
      //printf(". 1 .\n");
      list->head = new_node;
      list->tail = new_node;
      //printf("new tail\n");
      new_node->prev = NULL;
      new_node->next = NULL;
      list->size++;
      return true;
    }else{
      // 2. Enthesi stin arxi se gemati lista
      //printf(". 2 .\n");
      new_node->next = list->head;
      list->head->prev = new_node;
      list->head = new_node;
      list->size++;
      return true;
    }
  }else if (index == list->size) {
    // 3. enthesi sto telos tis listas
    new_node->next=NULL;
    new_node->prev=list->tail;
    list->tail = new_node;
    //printf("new tail\n");
    return true;
  }else{
    // 4. Enthesi se kathe alli periptwsi
    //printf("%d\n", index);
    //printf(". 3 .\n");
    i=0;
    tmp_node = list->head;
    while (i < index && tmp_node->next!=NULL){
            tmp_node = tmp_node->next;
            i++;
    }

    new_node->next = tmp_node;
    new_node->prev = tmp_node->prev;

    tmp_node->prev->next = new_node;
    tmp_node->prev = new_node;


    list->size++;
    return true;
  }
}

int index_of(dlist_t* list, type_t data) {
  //diatrexw tin lista ews to telos
  int index=0;
  list->cmp = student_cmp; // assign the function pointer to real function

  for(dnode_t* curr=list->head; curr!=NULL; curr=curr->next, index++) {
    if (list->cmp(curr->data,data) == 0) {
      //printf("same %d\n", index);
      return index;
    }
  }
  return -1;
}

int instances_of(dlist_t* list, type_t data) {
  int instances=0;
  list->cmp = student_cmp;
  for(dnode_t* curr=list->head; curr!=NULL; curr=curr->next) {
    if (list->cmp(curr->data,data) == 0) {
      instances++;
    }
  }
  return instances;
}

type_t get_index(dlist_t* list, int index) {
  // Elegxoi
  type_t zero_value = {0};
  //printf("index = %d list->size %d\n", index, list->size);
  if(index<0 || index>list->size){
    //printf("zero_value\n");
    return zero_value;
  }
  if (list->head==NULL) {
    exit(-1);
  }

  dnode_t* tmp_node=list->head;
  //printf("%d\n", tmp_node->data.aem);
  //ftanw sto epithimito index
  for (int i = 0; i <= list->size-1; i++) {
    //printf("%d\n", i);
    if (i==index) {
      //printf("edw\n");
      return tmp_node->data;
    }
    tmp_node=tmp_node->next;
  }
  return zero_value;
}

bool rmv(dlist_t* list, type_t data) {

  for(dnode_t* curr=list->head; curr!=NULL; curr=curr->next) {
    if (list->cmp(curr->data,data) == 0) {

      if (curr==list->head) {
        /* stin arxi */
        list->head = curr->next;
      } else if (curr->next==NULL) {
        /* sto telos */
        list->tail = curr->prev;
        curr->prev->next = NULL;
      }else{
        // diagrafi mesa stin lista
        curr->prev->next = curr->next;
        curr->next->prev = curr->prev;
        curr->next = curr->prev = NULL;
      }
      free(curr);
      list->size--;
      return true;
    }
  }
  return false;
}

type_t rmv_index(dlist_t* list, int index) {
  // Elegxoi
  type_t zero_value = {0};
  type_t data;
  dnode_t* tmp_node;
  int i;

  if(index<0 || index>list->size){
    //printf("zero_value\n");
    return zero_value;
  }
  if (list->head==NULL) {
    exit(-1);
  }


  if (index==0) {
    // diagrafi apo tin arxi tis listas
    data = list->head->data;
    tmp_node = list->head;
    //list->head->next->prev = NULL;
    list->head=list->head->next;

  }else if (index==list->size) {
    // diagrafi sto telos tis listas
    data = list->tail->data;
    tmp_node = list->tail;
    list->tail = list->tail->prev;

  }else{
    i=0;
    tmp_node = list->head;
    while (i < index && tmp_node->next!=NULL){
            tmp_node = tmp_node->next;
            i++;
    }
    data = tmp_node->data;

    tmp_node->prev->next = tmp_node->next;
    tmp_node->next->prev = tmp_node->prev;
    tmp_node->next = tmp_node->prev = NULL;
  }
  free(tmp_node);
  list->size--;
  return data;
}

void swap(dnode_t* n1, dnode_t* n2) {
  dnode_t* tmp_node;
  tmp_node = (dnode_t*)malloc(sizeof(dnode_t));
  tmp_node->data = n1->data;
  n1->data = n2->data;
  n2->data = tmp_node->data;
  free(tmp_node);
}

void catenate(dlist_t* list1, dlist_t* list2) {
  //dnode_t* tmp_node;

  if (list2->head==NULL) {
    exit(-1);
  }

  if (list1->head==NULL) {
    list1->head = list2->head;
    list1->tail = list2->tail;
    list1->tail->next = NULL;

    list2->head = list2->tail = NULL;
  }else{
    list1->tail->next = list2->head;
    list1->tail = list2->tail;
    list1->tail->next = NULL;

    list2->head = list2->tail = NULL;
  }
}

type_t* dlist2table(dlist_t* list) {
  type_t* table = (type_t*)malloc((list->size) * sizeof(type_t));
  if(!table) {
    fprintf(stderr, "Malloc failure [%s:%d]\n", __FILE__, __LINE__);
    exit(-1);
  }
  int i=0;
  while(size(list)>0) {
    table[i++] = get_index(list, 0);
    rmv_index(list,0);
  }
  return table;
}

void table2dlist(type_t table[], int table_size, dlist_t* list) {
    for(int i=0; i<table_size; i++) {
        insert(list, size(list), table[i]);
    }
    free(table);
}

void print(FILE* fp, dlist_t* list) {

    for(dnode_t* curr=list->head; curr!=NULL; curr=curr->next) {
      list->printer(fp, curr->data, false);
      putchar('\n');
    }
}
