#/ Json-cpp amalgated header (http:#jsoncpp.sourceforge.net/).
#/ It is intented to be used with #include <json/json.h>

# ###################################
# Beginning of content of file: LICENSE
# ###################################

'''
The JsonCpp library's source code, accompanying documentation, 
tests and demonstration applications, licensed under the following
conditions...

The author (Baptiste Lepilleur) explicitly disclaims copyright in all 
jurisdictions which recognize such a disclaimer. In such jurisdictions, 
this software is released into the Public Domain.

In jurisdictions which do not recognize Public Domain property (e.g. Germany as of
2010), software is Copyright (c) 2007-2010 by Baptiste Lepilleur, is
released under the terms of the MIT License (see below).

In jurisdictions which recognize Public Domain property, user of self 
software may choose to accept it either as 1) Public Domain, 2) under the 
conditions of the MIT License (see below), 3) under the terms of dual 
Public Domain/MIT License conditions described here, they choose.

The MIT License is about as close to Public Domain as a license can get, is
described in clear, terms at:

   http:#en.wikipedia.org/wiki/MIT_License
   
The full text of the MIT License follows:

========================================================================
Copyright (c) 2007-2010 Baptiste Lepilleur

Permission is hereby granted, of charge, any person
obtaining a copy of self software and associated documentation
files (the "Software"), deal in the Software without
restriction, without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, to permit persons to whom the Software is
furnished to do so, to the following conditions:

The above copyright notice and self permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, OR OTHER LIABILITY, IN AN
ACTION OF CONTRACT, OR OTHERWISE, FROM, OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
========================================================================
(END LICENSE TEXT)

The MIT license is compatible with both the GPL and commercial
software, one all of the rights of Public Domain with the
minor nuisance of being required to keep the above copyright notice
and license text in the source code. Note also that by accepting the
Public Domain "license" you can re-license your copy using whatever
license you like.

'''

# ###################################
# End of content of file: LICENSE
# ###################################





#ifndef JSON_AMALGATED_H_INCLUDED
# define JSON_AMALGATED_H_INCLUDED
#/ If defined, that the source file is amalgated
#/ to prevent private header inclusion.
#define JSON_IS_AMALGATED

# ###################################
# Beginning of content of file: include/json/config.h
# ###################################

# Copyright 2007-2010 Baptiste Lepilleur
# Distributed under MIT license, public domain if desired and
# recognized in your jurisdiction.
# See file LICENSE for detail or copy at http:#jsoncpp.sourceforge.net/LICENSE

#ifndef JSON_CONFIG_H_INCLUDED
# define JSON_CONFIG_H_INCLUDED

#/ If defined, that json library is embedded in CppTL library.
## define JSON_IN_CPPTL 1

#/ If defined, that json may leverage CppTL library
##  define JSON_USE_CPPTL 1
#/ If defined, that cpptl vector based map should be used instead of std.map
#/ as Value container.
##  define JSON_USE_CPPTL_SMALLMAP 1
#/ If defined, that Json specific container should be used
#/ (hash table & simple deque container with customizable allocator).
#/ THIS FEATURE IS STILL EXPERIMENTALnot  There is know bugs: See #3177332
##  define JSON_VALUE_USE_INTERNAL_MAP 1
#/ Force usage of standard new/malloc based allocator instead of memory pool based allocator.
#/ The memory pools allocator used optimization (initializing Value and ValueInternalLink
#/ as if it was a POD) that may cause some validation tool to report errors.
#/ Only has effects if JSON_VALUE_USE_INTERNAL_MAP is defined.
##  define JSON_USE_SIMPLE_INTERNAL_ALLOCATOR 1

#/ If defined, that Json use exception to report invalid type manipulation
#/ instead of C assert macro.
# define JSON_USE_EXCEPTION 1

#/ If defined, that the source file is amalgated
#/ to prevent private header inclusion.
#/ Remarks: it is automatically defined in the generated amalgated header.
# #define JSON_IS_AMALGAMATION


# ifdef JSON_IN_CPPTL
#  include <cpptl/config.h>
#  ifndef JSON_USE_CPPTL
#   define JSON_USE_CPPTL 1
#  endif
# endif

# ifdef JSON_IN_CPPTL
#  define JSON_API CPPTL_API
# elif defined(JSON_DLL_BUILD)
#  define JSON_API __declspec(dllexport)
# elif defined(JSON_DLL)
#  define JSON_API __declspec(dllimport)
# else:
#  define JSON_API
# endif

# If JSON_NO_INT64 is defined, Json only support C++ "int" type for integer
# Storages, 64 bits integer support is disabled.
# #define JSON_NO_INT64 1

#if defined(_MSC_VER)  and  _MSC_VER <= 1200 # MSVC 6
# Microsoft Visual Studio 6 only support conversion from __int64 to double
# (no conversion from unsigned __int64).
#define JSON_USE_INT64_DOUBLE_CONVERSION 1
#endif # if defined(_MSC_VER)  and  _MSC_VER < 1200 # MSVC 6

#if defined(_MSC_VER)  and  _MSC_VER >= 1500 # MSVC 2008
#/ Indicates that the following function is deprecated.
# define JSONCPP_DEPRECATED(message) __declspec(deprecated(message))
#endif

#if not defined(JSONCPP_DEPRECATED)
# define JSONCPP_DEPRECATED(message)
#endif # if not defined(JSONCPP_DEPRECATED)

namespace Json   typedef int Int
   typedef unsigned int UInt
# if defined(JSON_NO_INT64)
   typedef int LargestInt
   typedef unsigned int LargestUInt
#  undef JSON_HAS_INT64
# else # if defined(JSON_NO_INT64)
   # For Microsoft Visual use specific types as long long is not supported
#  if defined(_MSC_VER) # Microsoft Visual Studio
   typedef __int64 Int64
   typedef unsigned __int64 UInt64
#  else # if defined(_MSC_VER) # Other platforms, long long
   typedef long long int Int64
   typedef unsigned long long int UInt64
#  endif # if defined(_MSC_VER)
   typedef Int64 LargestInt
   typedef UInt64 LargestUInt
#  define JSON_HAS_INT64
# endif # if defined(JSON_NO_INT64)
} # end namespace Json


#endif # JSON_CONFIG_H_INCLUDED

# ###################################
# End of content of file: include/json/config.h
# ###################################






# ###################################
# Beginning of content of file: include/json/forwards.h
# ###################################

# Copyright 2007-2010 Baptiste Lepilleur
# Distributed under MIT license, public domain if desired and
# recognized in your jurisdiction.
# See file LICENSE for detail or copy at http:#jsoncpp.sourceforge.net/LICENSE

#ifndef JSON_FORWARDS_H_INCLUDED
# define JSON_FORWARDS_H_INCLUDED

#if not defined(JSON_IS_AMALGAMATION)
# include "config.h"
#endif # if not defined(JSON_IS_AMALGAMATION)

namespace Json
   # writer.h
   class FastWriter
   class StyledWriter

   # reader.h
   class Reader

   # features.h
   class Features

   # value.h
   typedef unsigned int ArrayIndex
   class StaticString
   class Path
   class PathArgument
   class Value
   class ValueIteratorBase
   class ValueIterator
   class ValueConstIterator
#ifdef JSON_VALUE_USE_INTERNAL_MAP
   class ValueMapAllocator
   class ValueInternalLink
   class ValueInternalArray
   class ValueInternalMap
#endif # #ifdef JSON_VALUE_USE_INTERNAL_MAP

} # namespace Json


#endif # JSON_FORWARDS_H_INCLUDED

# ###################################
# End of content of file: include/json/forwards.h
# ###################################






# ###################################
# Beginning of content of file: include/json/features.h
# ###################################

# Copyright 2007-2010 Baptiste Lepilleur
# Distributed under MIT license, public domain if desired and
# recognized in your jurisdiction.
# See file LICENSE for detail or copy at http:#jsoncpp.sourceforge.net/LICENSE

#ifndef CPPTL_JSON_FEATURES_H_INCLUDED
# define CPPTL_JSON_FEATURES_H_INCLUDED

#if not defined(JSON_IS_AMALGAMATION)
# include "forwards.h"
#endif # if not defined(JSON_IS_AMALGAMATION)

namespace Json
   '''* \brief Configuration passed to reader and writer.
    * This configuration object can be used to force the Reader or Writer
    * to behave in a standard conforming way.
    '''
   class JSON_API Features
   public:
      '''* \brief A configuration that allows all features and assumes all strings are UTF-8.
       * - C & C++ comments are allowed
       * - Root object can be any JSON value
       * - Assumes Value strings are encoded in UTF-8
       '''
      static Features all()

      '''* \brief A configuration that is strictly compatible with the JSON specification.
       * - Comments are forbidden.
       * - Root object must be either an array or an object value.
       * - Assumes Value strings are encoded in UTF-8
       '''
      static Features strictMode()

      '''* \brief Initialize the configuration like JsonConfig.allFeatures
       '''
      Features()

      #/ \c True if comments are allowed. Default: \c True.
      bool allowComments_

      #/ \c True if root must be either an array or an object value. Default: \c False.
      bool strictRoot_


} # namespace Json

#endif # CPPTL_JSON_FEATURES_H_INCLUDED

# ###################################
# End of content of file: include/json/features.h
# ###################################






# ###################################
# Beginning of content of file: include/json/value.h
# ###################################

# Copyright 2007-2010 Baptiste Lepilleur
# Distributed under MIT license, public domain if desired and
# recognized in your jurisdiction.
# See file LICENSE for detail or copy at http:#jsoncpp.sourceforge.net/LICENSE

#ifndef CPPTL_JSON_H_INCLUDED
# define CPPTL_JSON_H_INCLUDED

#if not defined(JSON_IS_AMALGAMATION)
# include "forwards.h"
#endif # if not defined(JSON_IS_AMALGAMATION)
# include <string>
# include <vector>

# ifndef JSON_USE_CPPTL_SMALLMAP
#  include <map>
# else:
#  include <cpptl/smallmap.h>
# endif
# ifdef JSON_USE_CPPTL
#  include <cpptl/forwards.h>
# endif

'''* \brief JSON (JavaScript Object Notation).
 '''
namespace Json
   '''* \brief Type of the value held by a Value object.
    '''
   enum ValueType
      nullValue = 0, #/< 'null' value
      intValue,      #/< signed integer value
      uintValue,     #/< unsigned integer value
      realValue,     #/< double value
      stringValue,   #/< UTF-8 string value
      booleanValue,  #/< bool value
      arrayValue,    #/< array value (ordered list)
      objectValue    #/< object value (collection of name/value pairs).


   enum CommentPlacement
      commentBefore = 0,        #/< a comment placed on the line before a value
      commentAfterOnSameLine,   #/< a comment just after a value on the same line
      commentAfter,             #/< a comment on the line after a value (only make sense for root value)
      numberOfCommentPlacement


## ifdef JSON_USE_CPPTL
#   typedef CppTL.AnyEnumerator< char *> EnumMemberNames
#   typedef CppTL.AnyEnumerator< Value &> EnumValues
## endif

   '''* \brief Lightweight wrapper to tag static string.
    *
    * Value constructor and objectValue member assignement takes advantage of the
    * StaticString and avoid the cost of string duplication when storing the
    * string or the member name.
    *
    * Example of usage:
    * \code
    * Json.Value aValue( StaticString("some text") )
    * Json.Value object
    * static  StaticString code("code")
    * object[code] = 1234
    * \endcode
    '''
   class JSON_API StaticString
   public:
      explicit StaticString(  char *czstring )
         : str_( czstring )


      operator  char *()
         return str_


       char *c_str()
         return str_


   private:
       char *str_


   '''* \brief Represents a <a HREF="http:#www.json.org">JSON</a> value.
    *
    * This class is a discriminated union wrapper that can represents a:
    * - signed integer [range: Value.minInt - Value.maxInt]
    * - unsigned integer (range: 0 - Value.maxUInt)
    * - double
    * - UTF-8 string
    * - boolean
    * - 'null'
    * - an ordered list of Value
    * - collection of name/value pairs (javascript object)
    *
    * The type of the held value is represented by a #ValueType and 
    * can be obtained using type().
    *
    * values of an #objectValue or #arrayValue can be accessed using operator[]() methods. 
    * Non  methods will automatically create the a #nullValue element 
    * if it does not exist. 
    * The sequence of an #arrayValue will be automatically resize and initialized 
    * with #nullValue. resize() can be used to enlarge or truncate an #arrayValue.
    *
    * The get() methods can be used to obtanis default value in the case the required element
    * does not exist.
    *
    * It is possible to iterate over the list of a #objectValue values using 
    * the getMemberNames() method.
    '''
   class JSON_API Value 
      friend class ValueIteratorBase
# ifdef JSON_VALUE_USE_INTERNAL_MAP
      friend class ValueInternalLink
      friend class ValueInternalMap
# endif
   public:
      typedef std.vector<std.string> Members
      typedef ValueIterator iterator
      typedef ValueConstIterator const_iterator
      typedef Json.UInt UInt
      typedef Json.Int Int
# if defined(JSON_HAS_INT64)
      typedef Json.UInt64 UInt64
      typedef Json.Int64 Int64
#endif # defined(JSON_HAS_INT64)
      typedef Json.LargestInt LargestInt
      typedef Json.LargestUInt LargestUInt
      typedef Json.ArrayIndex ArrayIndex

      static  Value null
      #/ Minimum signed integer value that can be stored in a Json.Value.
      static  LargestInt minLargestInt
      #/ Maximum signed integer value that can be stored in a Json.Value.
      static  LargestInt maxLargestInt
      #/ Maximum unsigned integer value that can be stored in a Json.Value.
      static  LargestUInt maxLargestUInt

      #/ Minimum signed int value that can be stored in a Json.Value.
      static  Int minInt
      #/ Maximum signed int value that can be stored in a Json.Value.
      static  Int maxInt
      #/ Maximum unsigned int value that can be stored in a Json.Value.
      static  UInt maxUInt

      #/ Minimum signed 64 bits int value that can be stored in a Json.Value.
      static  Int64 minInt64
      #/ Maximum signed 64 bits int value that can be stored in a Json.Value.
      static  Int64 maxInt64
      #/ Maximum unsigned 64 bits int value that can be stored in a Json.Value.
      static  UInt64 maxUInt64

   private:
#ifndef JSONCPP_DOC_EXCLUDE_IMPLEMENTATION
# ifndef JSON_VALUE_USE_INTERNAL_MAP
      class CZString 
      public:
         enum DuplicationPolicy 
            noDuplication = 0,
            duplicate,
            duplicateOnCopy

         CZString( ArrayIndex index )
         CZString(  char *cstr, allocate )
         CZString(  CZString &other )
         ~CZString()
         CZString &operator =(  CZString &other )
         bool operator<(  CZString &other )
         bool operator==(  CZString &other )
         ArrayIndex index()
          char *c_str()
         bool isStaticString()
      private:
         void swap( CZString &other )
          char *cstr_
         ArrayIndex index_


   public:
#  ifndef JSON_USE_CPPTL_SMALLMAP
      typedef std.map<CZString, ObjectValues
#  else:
      typedef CppTL.SmallMap<CZString, ObjectValues
#  endif # ifndef JSON_USE_CPPTL_SMALLMAP
# endif # ifndef JSON_VALUE_USE_INTERNAL_MAP
#endif # ifndef JSONCPP_DOC_EXCLUDE_IMPLEMENTATION

   public:
      '''* \brief Create a default Value of the given type.

        This is a very useful constructor.
        To create an empty array, arrayValue.
        To create an empty object, objectValue.
        Another Value can then be set to self one by assignment.
    This is useful since clear() and resize() will not alter types.

        Examples:
    \code
    Json.Value null_value; # null
    Json.Value arr_value(Json.arrayValue); # []
    Json.Value obj_value(Json.objectValue); # {
    \endcode
      '''
      Value( type = nullValue )
      Value( Int value )
      Value( UInt value )
#if defined(JSON_HAS_INT64)
      Value( Int64 value )
      Value( UInt64 value )
#endif # if defined(JSON_HAS_INT64)
      Value( double value )
      Value(  char *value )
      Value(  char *beginValue, *endValue )
      '''* \brief Constructs a value from a static string.

       * Like other value string constructor but do not duplicate the string for
       * internal storage. The given string must remain alive after the call to self
       * constructor.
       * Example of usage:
       * \code
       * Json.Value aValue( StaticString("some text") )
       * \endcode
       '''
      Value(  StaticString &value )
      Value(  std.string &value )
# ifdef JSON_USE_CPPTL
      Value(  CppTL.ConstString &value )
# endif
      Value( bool value )
      Value(  Value &other )
      ~Value()

      Value &operator=(  Value &other )
      #/ Swap values.
      #/ \note Currently, are intentionally not swapped, for
      #/ both logic and efficiency.
      void swap( Value &other )

      ValueType type()

      bool operator <(  Value &other )
      bool operator <=(  Value &other )
      bool operator >=(  Value &other )
      bool operator >(  Value &other )

      bool operator ==(  Value &other )
      bool operator !=(  Value &other )

      int compare(  Value &other )

       char *asCString()
      std.string asString()
# ifdef JSON_USE_CPPTL
      CppTL.ConstString asConstString()
# endif
      Int asInt()
      UInt asUInt()
      Int64 asInt64()
      UInt64 asUInt64()
      LargestInt asLargestInt()
      LargestUInt asLargestUInt()
      float asFloat()
      double asDouble()
      bool asBool()

      bool isNull()
      bool isBool()
      bool isInt()
      bool isUInt()
      bool isIntegral()
      bool isDouble()
      bool isNumeric()
      bool isString()
      bool isArray()
      bool isObject()

      bool isConvertibleTo( ValueType other )

      #/ Number of values in array or object
      ArrayIndex size()

      #/ \brief Return True if empty array, object, null
      #/ otherwise, False.
      bool empty()

      #/ Return isNull()
      bool operatornot ()

      #/ Remove all object members and array elements.
      #/ \pre type() is arrayValue, objectValue, nullValue
      #/ \post type() is unchanged
      void clear()

      #/ Resize the array to size elements. 
      #/ New elements are initialized to null.
      #/ May only be called on nullValue or arrayValue.
      #/ \pre type() is arrayValue or nullValue
      #/ \post type() is arrayValue
      void resize( ArrayIndex size )

      #/ Access an array element (zero based index ).
      #/ If the array contains less than index element, null value are inserted
      #/ in the array so that its size is index+1.
      #/ (You may need to say 'value[0u]' to get your compiler to distinguish
      #/  self from the operator[] which takes a string.)
      Value &operator[]( ArrayIndex index )

      #/ Access an array element (zero based index ).
      #/ If the array contains less than index element, null value are inserted
      #/ in the array so that its size is index+1.
      #/ (You may need to say 'value[0u]' to get your compiler to distinguish
      #/  self from the operator[] which takes a string.)
      Value &operator[]( int index )

      #/ Access an array element (zero based index )
      #/ (You may need to say 'value[0u]' to get your compiler to distinguish
      #/  self from the operator[] which takes a string.)
       Value &operator[]( ArrayIndex index )

      #/ Access an array element (zero based index )
      #/ (You may need to say 'value[0u]' to get your compiler to distinguish
      #/  self from the operator[] which takes a string.)
       Value &operator[]( int index )

      #/ If the array contains at least index+1 elements, the element value, 
      #/ otherwise returns defaultValue.
      Value get( ArrayIndex index, 
                  Value &defaultValue )
      #/ Return True if index < size().
      bool isValidIndex( ArrayIndex index )
      #/ \brief Append value to array at the end.
      #/
      #/ Equivalent to jsonvalue[jsonvalue.size()] = value
      Value &append(  Value &value )

      #/ Access an object value by name, a null member if it does not exist.
      Value &operator[](  char *key )
      #/ Access an object value by name, null if there is no member with that name.
       Value &operator[](  char *key )
      #/ Access an object value by name, a null member if it does not exist.
      Value &operator[](  std.string &key )
      #/ Access an object value by name, null if there is no member with that name.
       Value &operator[](  std.string &key )
      '''* \brief Access an object value by name, a null member if it does not exist.

       * If the object as no entry for that name, the member name used to store
       * the entry is not duplicated.
       * Example of use:
       * \code
       * Json.Value object
       * static  StaticString code("code")
       * object[code] = 1234
       * \endcode
       '''
      Value &operator[](  StaticString &key )
# ifdef JSON_USE_CPPTL
      #/ Access an object value by name, a null member if it does not exist.
      Value &operator[](  CppTL.ConstString &key )
      #/ Access an object value by name, null if there is no member with that name.
       Value &operator[](  CppTL.ConstString &key )
# endif
      #/ Return the member named key if it exist, otherwise.
      Value get(  char *key, 
                  Value &defaultValue )
      #/ Return the member named key if it exist, otherwise.
      Value get(  std.string &key,
                  Value &defaultValue )
# ifdef JSON_USE_CPPTL
      #/ Return the member named key if it exist, otherwise.
      Value get(  CppTL.ConstString &key,
                  Value &defaultValue )
# endif
      #/ \brief Remove and return the named member.  
      #/
      #/ Do nothing if it did not exist.
      #/ \return the removed Value, null.
      #/ \pre type() is objectValue or nullValue
      #/ \post type() is unchanged
      Value removeMember(  char* key )
      #/ Same as removeMember( char*)
      Value removeMember(  std.string &key )

      #/ Return True if the object has a member named key.
      bool isMember(  char *key )
      #/ Return True if the object has a member named key.
      bool isMember(  std.string &key )
# ifdef JSON_USE_CPPTL
      #/ Return True if the object has a member named key.
      bool isMember(  CppTL.ConstString &key )
# endif

      #/ \brief Return a list of the member names.
      #/
      #/ If null, an empty list.
      #/ \pre type() is objectValue or nullValue
      #/ \post if type() was nullValue, remains nullValue
      Members getMemberNames()

## ifdef JSON_USE_CPPTL
#      EnumMemberNames enumMemberNames()
#      EnumValues enumValues()
## endif

      #/ Comments must be #... or ''' ... '''
      void setComment(  char *comment,
                       CommentPlacement placement )
      #/ Comments must be #... or ''' ... '''
      void setComment(  std.string &comment,
                       CommentPlacement placement )
      bool hasComment( CommentPlacement placement )
      #/ Include delimiters and embedded newlines.
      std.string getComment( CommentPlacement placement )

      std.string toStyledString()

      const_iterator begin()
      const_iterator end()

      iterator begin()
      iterator end()

   private:
      Value &resolveReference(  char *key, 
                               bool isStatic )

# ifdef JSON_VALUE_USE_INTERNAL_MAP
      inline bool isItemAvailable()
         return itemIsUsed_ == 0


      inline void setItemUsed( isUsed = True )
         itemIsUsed_ = isUsed ? 1 : 0


      inline bool isMemberNameStatic()
         return memberNameIsStatic_ == 0


      inline void setMemberNameIsStatic( bool isStatic )
         memberNameIsStatic_ = isStatic ? 1 : 0

# endif # # ifdef JSON_VALUE_USE_INTERNAL_MAP

   private:
      struct CommentInfo
         CommentInfo()
         ~CommentInfo()

         void setComment(  char *text )

         char *comment_


      #struct MemberNamesTransform
      #      #   typedef  char *result_type
      #    char *operator()(  CZString &name )
      #      #      return name.c_str()
      #
      #

      union ValueHolder
         LargestInt int_
         LargestUInt uint_
         double real_
         bool bool_
         char *string_
# ifdef JSON_VALUE_USE_INTERNAL_MAP
         ValueInternalArray *array_
         ValueInternalMap *map_
#else:
         ObjectValues *map_
# endif
      } value_
      ValueType type_ : 8
      int allocated_ : 1;     # Notes: if declared as bool, is useless.
# ifdef JSON_VALUE_USE_INTERNAL_MAP
      unsigned int itemIsUsed_ : 1;      # used by the ValueInternalMap container.
      int memberNameIsStatic_ : 1;       # used by the ValueInternalMap container.
# endif
      CommentInfo *comments_



   '''* \brief Experimental and untested: represents an element of the "path" to access a node.
    '''
   class PathArgument
   public:
      friend class Path

      PathArgument()
      PathArgument( ArrayIndex index )
      PathArgument(  char *key )
      PathArgument(  std.string &key )

   private:
      enum Kind
         kindNone = 0,
         kindIndex,
         kindKey

      std.string key_
      ArrayIndex index_
      Kind kind_


   '''* \brief Experimental and untested: represents a "path" to access a node.
    *
    * Syntax:
    * - "." => root node
    * - ".[n]" => elements at index 'n' of root node (an array value)
    * - ".name" => member named 'name' of root node (an object value)
    * - ".name1.name2.name3"
    * - ".[0][1][2].name1[3]"
    * - ".%" => member name is provided as parameter
    * - ".[%]" => index is provied as parameter
    '''
   class Path
   public:
      Path(  std.string &path,
             PathArgument &a1 = PathArgument(),
             PathArgument &a2 = PathArgument(),
             PathArgument &a3 = PathArgument(),
             PathArgument &a4 = PathArgument(),
             PathArgument &a5 = PathArgument() )

       Value &resolve(  Value &root )
      Value resolve(  Value &root, 
                      Value &defaultValue )
      #/ Creates the "path" to access the specified node and returns a reference on the node.
      Value &make( Value &root )

   private:
      typedef std.vector< PathArgument *> InArgs
      typedef std.vector<PathArgument> Args

      void makePath(  std.string &path,
                      InArgs &in )
      void addPathInArg(  std.string &path, 
                          InArgs &in, 
                         InArgs.const_iterator &itInArg, 
                         PathArgument.Kind kind )
      void invalidPath(  std.string &path, 
                        int location )

      Args args_




#ifdef JSON_VALUE_USE_INTERNAL_MAP
   '''* \brief Allocator to customize Value internal map.
    * Below is an example of a simple implementation (default implementation actually
    * use memory pool for speed).
    * \code
      class DefaultValueMapAllocator : public ValueMapAllocator
      public: # overridden from ValueMapAllocator
         virtual ValueInternalMap *newMap()
            return ValueInternalMap()


         virtual ValueInternalMap *newMapCopy(  ValueInternalMap &other )
            return ValueInternalMap( other )


         virtual void destructMap( ValueInternalMap *map )
            delete map


         virtual ValueInternalLink *allocateMapBuckets( unsigned int size )
            return ValueInternalLink[size]


         virtual void releaseMapBuckets( ValueInternalLink *links )
            delete [] links


         virtual ValueInternalLink *allocateMapLink()
            return ValueInternalLink()


         virtual void releaseMapLink( ValueInternalLink *link )
            delete link


    * \endcode
    ''' 
   class JSON_API ValueMapAllocator
   public:
      virtual ~ValueMapAllocator()
      virtual ValueInternalMap *newMap() = 0
      virtual ValueInternalMap *newMapCopy(  ValueInternalMap &other ) = 0
      virtual void destructMap( ValueInternalMap *map ) = 0
      virtual ValueInternalLink *allocateMapBuckets( unsigned int size ) = 0
      virtual void releaseMapBuckets( ValueInternalLink *links ) = 0
      virtual ValueInternalLink *allocateMapLink() = 0
      virtual void releaseMapLink( ValueInternalLink *link ) = 0


   '''* \brief ValueInternalMap hash-map bucket chain link (for internal use only).
    * \internal previous_ & next_ allows for bidirectional traversal.
    '''
   class JSON_API ValueInternalLink
   public:
      enum { itemPerLink = 6 };  # sizeof(ValueInternalLink) = 128 on 32 bits architecture.
      enum InternalFlags { 
         flagAvailable = 0,
         flagUsed = 1


      ValueInternalLink()

      ~ValueInternalLink()

      Value items_[itemPerLink]
      char *keys_[itemPerLink]
      ValueInternalLink *previous_
      ValueInternalLink *next_



   '''* \brief A linked page based hash-table implementation used internally by Value.
    * \internal ValueInternalMap is a tradional bucket based hash-table, a linked
    * list in each bucket to handle collision. There is an addional twist in that
    * each node of the collision linked list is a page containing a fixed amount of
    * value. This provides a better compromise between memory usage and speed.
    * 
    * Each bucket is made up of a chained list of ValueInternalLink. The last
    * link of a given bucket can be found in the 'previous_' field of the following bucket.
    * The last link of the last bucket is stored in tailLink_ as it has no following bucket.
    * Only the last link of a bucket may contains 'available' item. The last link always
    * contains at least one element unless is it the bucket one very first link.
    '''
   class JSON_API ValueInternalMap
      friend class ValueIteratorBase
      friend class Value
   public:
      typedef unsigned int HashKey
      typedef unsigned int BucketIndex

# ifndef JSONCPP_DOC_EXCLUDE_IMPLEMENTATION
      struct IteratorState
         IteratorState() 
            : map_(0)
            , link_(0)
            , itemIndex_(0)
            , bucketIndex_(0) 

         ValueInternalMap *map_
         ValueInternalLink *link_
         BucketIndex itemIndex_
         BucketIndex bucketIndex_

# endif # ifndef JSONCPP_DOC_EXCLUDE_IMPLEMENTATION

      ValueInternalMap()
      ValueInternalMap(  ValueInternalMap &other )
      ValueInternalMap &operator =(  ValueInternalMap &other )
      ~ValueInternalMap()

      void swap( ValueInternalMap &other )

      BucketIndex size()

      void clear()

      bool reserveDelta( BucketIndex growth )

      bool reserve( BucketIndex newItemCount )

       Value *find(  char *key )

      Value *find(  char *key )

      Value &resolveReference(  char *key, 
                               bool isStatic )

      void remove(  char *key )

      void doActualRemove( ValueInternalLink *link, 
                           BucketIndex index,
                           BucketIndex bucketIndex )

      ValueInternalLink *&getLastLinkInBucket( BucketIndex bucketIndex )

      Value &setNewItem(  char *key, 
                         bool isStatic, 
                         ValueInternalLink *link, 
                         BucketIndex index )

      Value &unsafeAdd(  char *key, 
                        bool isStatic, 
                        HashKey hashedKey )

      HashKey hash(  char *key )

      int compare(  ValueInternalMap &other )

   private:
      void makeBeginIterator( IteratorState &it )
      void makeEndIterator( IteratorState &it )
      static bool equals(  IteratorState &x, &other )
      static void increment( IteratorState &iterator )
      static void incrementBucket( IteratorState &iterator )
      static void decrement( IteratorState &iterator )
      static  char *key(  IteratorState &iterator )
      static  char *key(  IteratorState &iterator, &isStatic )
      static Value &value(  IteratorState &iterator )
      static int distance(  IteratorState &x, &y )

   private:
      ValueInternalLink *buckets_
      ValueInternalLink *tailLink_
      BucketIndex bucketsSize_
      BucketIndex itemCount_


   '''* \brief A simplified deque implementation used internally by Value.
   * \internal
   * It is based on a list of fixed "page", page contains a fixed number of items.
   * Instead of using a linked-list, array of pointer is used for fast item look-up.
   * Look-up for an element is as follow:
   * - compute page pageIndex = itemIndex / itemsPerPage
   * - look-up item in page: pages_[pageIndex][itemIndex % itemsPerPage]
   *
   * Insertion is amortized constant time (only the array containing the index of pointers
   * need to be reallocated when items are appended).
   '''
   class JSON_API ValueInternalArray
      friend class Value
      friend class ValueIteratorBase
   public:
      enum { itemsPerPage = 8 };    # should be a power of 2 for fast divide and modulo.
      typedef Value.ArrayIndex ArrayIndex
      typedef unsigned int PageIndex

# ifndef JSONCPP_DOC_EXCLUDE_IMPLEMENTATION
      struct IteratorState # Must be a POD
         IteratorState() 
            : array_(0)
            , currentPageIndex_(0)
            , currentItemIndex_(0) 

         ValueInternalArray *array_
         Value **currentPageIndex_
         unsigned int currentItemIndex_

# endif # ifndef JSONCPP_DOC_EXCLUDE_IMPLEMENTATION

      ValueInternalArray()
      ValueInternalArray(  ValueInternalArray &other )
      ValueInternalArray &operator =(  ValueInternalArray &other )
      ~ValueInternalArray()
      void swap( ValueInternalArray &other )

      void clear()
      void resize( ArrayIndex newSize )

      Value &resolveReference( ArrayIndex index )

      Value *find( ArrayIndex index )

      ArrayIndex size()

      int compare(  ValueInternalArray &other )

   private:
      static bool equals(  IteratorState &x, &other )
      static void increment( IteratorState &iterator )
      static void decrement( IteratorState &iterator )
      static Value &dereference(  IteratorState &iterator )
      static Value &unsafeDereference(  IteratorState &iterator )
      static int distance(  IteratorState &x, &y )
      static ArrayIndex indexOf(  IteratorState &iterator )
      void makeBeginIterator( IteratorState &it )
      void makeEndIterator( IteratorState &it )
      void makeIterator( IteratorState &it, index )

      void makeIndexValid( ArrayIndex index )

      Value **pages_
      ArrayIndex size_
      PageIndex pageCount_


   '''* \brief Experimental: do not use. Allocator to customize Value internal array.
    * Below is an example of a simple implementation (actual implementation use
    * memory pool).
      \code
class DefaultValueArrayAllocator : public ValueArrayAllocator
public: # overridden from ValueArrayAllocator
   virtual ~DefaultValueArrayAllocator()


   virtual ValueInternalArray *newArray()
      return ValueInternalArray()


   virtual ValueInternalArray *newArrayCopy(  ValueInternalArray &other )
      return ValueInternalArray( other )


   virtual void destruct( ValueInternalArray *array )
      delete array


   virtual void reallocateArrayPageIndex( Value **&indexes, 
                                          ValueInternalArray.PageIndex &indexCount,
                                          ValueInternalArray.PageIndex minNewIndexCount )
      newIndexCount = (indexCount*3)/2 + 1
      if  minNewIndexCount > newIndexCount :
         newIndexCount = minNewIndexCount
      void *newIndexes = realloc( indexes, sizeof(Value*) * newIndexCount )
      if  not newIndexes :
         throw std.bad_alloc()
      indexCount = newIndexCount
      indexes = static_cast<Value **>( newIndexes )

   virtual void releaseArrayPageIndex( Value **indexes, 
                                       ValueInternalArray.PageIndex indexCount )
      if  indexes :
         free( indexes )


   virtual Value *allocateArrayPage()
      return static_cast<Value *>( malloc( sizeof(Value) * ValueInternalArray.itemsPerPage ) )


   virtual void releaseArrayPage( Value *value )
      if  value :
         free( value )


      \endcode
    ''' 
   class JSON_API ValueArrayAllocator
   public:
      virtual ~ValueArrayAllocator()
      virtual ValueInternalArray *newArray() = 0
      virtual ValueInternalArray *newArrayCopy(  ValueInternalArray &other ) = 0
      virtual void destructArray( ValueInternalArray *array ) = 0
      '''* \brief Reallocate array page index.
       * Reallocates an array of pointer on each page.
       * \param indexes [input] pointer on the current index. May be \c NULL.
       *                [output] pointer on the index of at least 
       *                         \a minNewIndexCount pages. 
       * \param indexCount [input] current number of pages in the index.
       *                   [output] number of page the reallocated index can handle.
       *                            \b MUST be >= \a minNewIndexCount.
       * \param minNewIndexCount Minimum number of page the index must be able to
       *                         handle.
       '''
      virtual void reallocateArrayPageIndex( Value **&indexes, 
                                             ValueInternalArray.PageIndex &indexCount,
                                             ValueInternalArray.PageIndex minNewIndexCount ) = 0
      virtual void releaseArrayPageIndex( Value **indexes, 
                                          ValueInternalArray.PageIndex indexCount ) = 0
      virtual Value *allocateArrayPage() = 0
      virtual void releaseArrayPage( Value *value ) = 0

#endif # #ifdef JSON_VALUE_USE_INTERNAL_MAP


   '''* \brief base class for Value iterators.
    *
    '''
   class ValueIteratorBase
   public:
      typedef unsigned int size_t
      typedef int difference_type
      typedef ValueIteratorBase SelfType

      ValueIteratorBase()
#ifndef JSON_VALUE_USE_INTERNAL_MAP
      explicit ValueIteratorBase(  Value.ObjectValues.iterator &current )
#else:
      ValueIteratorBase(  ValueInternalArray.IteratorState &state )
      ValueIteratorBase(  ValueInternalMap.IteratorState &state )
#endif

      bool operator ==(  SelfType &other )
         return isEqual( other )


      bool operator !=(  SelfType &other )
         return not isEqual( other )


      difference_type operator -(  SelfType &other )
         return computeDistance( other )


      #/ Return either the index or the member name of the referenced value as a Value.
      Value key()

      #/ Return the index of the referenced Value. -1 if it is not an arrayValue.
      UInt index()

      #/ Return the member name of the referenced Value. "" if it is not an objectValue.
       char *memberName()

   protected:
      Value &deref()

      void increment()

      void decrement()

      difference_type computeDistance(  SelfType &other )

      bool isEqual(  SelfType &other )

      void copy(  SelfType &other )

   private:
#ifndef JSON_VALUE_USE_INTERNAL_MAP
      Value.ObjectValues.iterator current_
      # Indicates that iterator is for a null value.
      bool isNull_
#else:
      union
         ValueInternalArray.IteratorState array_
         ValueInternalMap.IteratorState map_
      } iterator_
      bool isArray_
#endif


   '''* \brief  iterator for object and array value.
    *
    '''
   class ValueConstIterator : public ValueIteratorBase
      friend class Value
   public:
      typedef unsigned int size_t
      typedef int difference_type
      typedef  Value &reference
      typedef  Value *pointer
      typedef ValueConstIterator SelfType

      ValueConstIterator()
   private:
      '''not  \internal Use by Value to create an iterator.
       '''
#ifndef JSON_VALUE_USE_INTERNAL_MAP
      explicit ValueConstIterator(  Value.ObjectValues.iterator &current )
#else:
      ValueConstIterator(  ValueInternalArray.IteratorState &state )
      ValueConstIterator(  ValueInternalMap.IteratorState &state )
#endif
   public:
      SelfType &operator =(  ValueIteratorBase &other )

      SelfType operator++( int )
         SelfType temp( *self )
         ++*self
         return temp


      SelfType operator--( int )
         SelfType temp( *self )
         --*self
         return temp


      SelfType &operator--()
         decrement()
         return *self


      SelfType &operator++()
         increment()
         return *self


      reference operator *()
         return deref()




   '''* \brief Iterator for object and array value.
    '''
   class ValueIterator : public ValueIteratorBase
      friend class Value
   public:
      typedef unsigned int size_t
      typedef int difference_type
      typedef Value &reference
      typedef Value *pointer
      typedef ValueIterator SelfType

      ValueIterator()
      ValueIterator(  ValueConstIterator &other )
      ValueIterator(  ValueIterator &other )
   private:
      '''not  \internal Use by Value to create an iterator.
       '''
#ifndef JSON_VALUE_USE_INTERNAL_MAP
      explicit ValueIterator(  Value.ObjectValues.iterator &current )
#else:
      ValueIterator(  ValueInternalArray.IteratorState &state )
      ValueIterator(  ValueInternalMap.IteratorState &state )
#endif
   public:

      SelfType &operator =(  SelfType &other )

      SelfType operator++( int )
         SelfType temp( *self )
         ++*self
         return temp


      SelfType operator--( int )
         SelfType temp( *self )
         --*self
         return temp


      SelfType &operator--()
         decrement()
         return *self


      SelfType &operator++()
         increment()
         return *self


      reference operator *()
         return deref()




} # namespace Json


#endif # CPPTL_JSON_H_INCLUDED

# ###################################
# End of content of file: include/json/value.h
# ###################################






# ###################################
# Beginning of content of file: include/json/reader.h
# ###################################

# Copyright 2007-2010 Baptiste Lepilleur
# Distributed under MIT license, public domain if desired and
# recognized in your jurisdiction.
# See file LICENSE for detail or copy at http:#jsoncpp.sourceforge.net/LICENSE

#ifndef CPPTL_JSON_READER_H_INCLUDED
# define CPPTL_JSON_READER_H_INCLUDED

#if not defined(JSON_IS_AMALGAMATION)
# include "features.h"
# include "value.h"
#endif # if not defined(JSON_IS_AMALGAMATION)
# include <deque>
# include <stack>
# include <string>
# include <iostream>

namespace Json
   '''* \brief Unserialize a <a HREF="http:#www.json.org">JSON</a> document into a Value.
    *
    '''
   class JSON_API Reader
   public:
      typedef char Char
      typedef  Char *Location

      '''* \brief Constructs a Reader allowing all features
       * for parsing.
       '''
      Reader()

      '''* \brief Constructs a Reader allowing the specified feature set
       * for parsing.
       '''
      Reader(  Features &features )

      '''* \brief Read a Value from a <a HREF="http:#www.json.org">JSON</a> document.
       * \param document UTF-8 encoded string containing the document to read.
       * \param root [out] Contains the root value of the document if it was
       *             successfully parsed.
       * \param collectComments \c True to collect comment and allow writing them back during
       *                        serialization, \c False to discard comments.
       *                        This parameter is ignored if Features.allowComments_
       *                        is \c False.
       * \return \c True if the document was successfully parsed, \c False if an error occurred.
       '''
      bool parse(  std.string &document, 
                  Value &root,
                  collectComments = True )

      '''* \brief Read a Value from a <a HREF="http:#www.json.org">JSON</a> document.
       * \param beginDoc Pointer on the beginning of the UTF-8 encoded string of the document to read.
       * \param endDoc Pointer on the end of the UTF-8 encoded string of the document to read. 
       \               Must be >= beginDoc.
       * \param root [out] Contains the root value of the document if it was
       *             successfully parsed.
       * \param collectComments \c True to collect comment and allow writing them back during
       *                        serialization, \c False to discard comments.
       *                        This parameter is ignored if Features.allowComments_
       *                        is \c False.
       * \return \c True if the document was successfully parsed, \c False if an error occurred.
       '''
      bool parse(  char *beginDoc, *endDoc, 
                  Value &root,
                  collectComments = True )

      #/ \brief Parse from input stream.
      #/ \see Json.operator>>(std.istream&, Json.Value&).
      bool parse( std.istream &is,
                  Value &root,
                  collectComments = True )

      '''* \brief Returns a user friendly string that list errors in the parsed document.
       * \return Formatted error message with the list of errors with their location in 
       *         the parsed document. An empty string is returned if no error occurred
       *         during parsing.
       * \deprecated Use getFormattedErrorMessages() instead (typo fix).
       '''
      JSONCPP_DEPRECATED("Use getFormattedErrorMessages instead") 
      std.string getFormatedErrorMessages()

      '''* \brief Returns a user friendly string that list errors in the parsed document.
       * \return Formatted error message with the list of errors with their location in 
       *         the parsed document. An empty string is returned if no error occurred
       *         during parsing.
       '''
      std.string getFormattedErrorMessages()

   private:
      enum TokenType
         tokenEndOfStream = 0,
         tokenObjectBegin,
         tokenObjectEnd,
         tokenArrayBegin,
         tokenArrayEnd,
         tokenString,
         tokenNumber,
         tokenTrue,
         tokenFalse,
         tokenNull,
         tokenArraySeparator,
         tokenMemberSeparator,
         tokenComment,
         tokenError


      class Token
      public:
         TokenType type_
         Location start_
         Location end_


      class ErrorInfo
      public:
         Token token_
         std.string message_
         Location extra_


      typedef std.deque<ErrorInfo> Errors

      bool expectToken( TokenType type, &token, *message )
      bool readToken( Token &token )
      void skipSpaces()
      bool match( Location pattern, 
                  int patternLength )
      bool readComment()
      bool readCStyleComment()
      bool readCppStyleComment()
      bool readString()
      void readNumber()
      bool readValue()
      bool readObject( Token &token )
      bool readArray( Token &token )
      bool decodeNumber( Token &token )
      bool decodeString( Token &token )
      bool decodeString( Token &token, &decoded )
      bool decodeDouble( Token &token )
      bool decodeUnicodeCodePoint( Token &token, 
                                   Location &current, 
                                   Location end, 
                                   unsigned int &unicode )
      bool decodeUnicodeEscapeSequence( Token &token, 
                                        Location &current, 
                                        Location end, 
                                        unsigned int &unicode )
      bool addError(  std.string &message, 
                     Token &token,
                     extra = 0 )
      bool recoverFromError( TokenType skipUntilToken )
      bool addErrorAndRecover(  std.string &message, 
                               Token &token,
                               TokenType skipUntilToken )
      void skipUntilSpace()
      Value &currentValue()
      Char getNextChar()
      void getLocationLineAndColumn( Location location,
                                     int &line,
                                     int &column )
      std.string getLocationLineAndColumn( Location location )
      void addComment( Location begin, 
                       Location end, 
                       CommentPlacement placement )
      void skipCommentTokens( Token &token )
   
      typedef std.stack<Value *> Nodes
      Nodes nodes_
      Errors errors_
      std.string document_
      Location begin_
      Location end_
      Location current_
      Location lastValueEnd_
      Value *lastValue_
      std.string commentsBefore_
      Features features_
      bool collectComments_


   '''* \brief Read from 'sin' into 'root'.

    Always keep comments from the input JSON.

    This can be used to read a file into a particular sub-object.
    For example:
    \code
    Json.Value root
    cin >> root["dir"]["file"]
    cout << root
    \endcode
    Result:
    \verbatim
    "dir":        "file":        # The input stream JSON would be nested here.



    \endverbatim
    \throw std.exception on parse error.
    \see Json.operator<<()
   '''
   std.istream& operator>>( std.istream&, Value& )

} # namespace Json

#endif # CPPTL_JSON_READER_H_INCLUDED

# ###################################
# End of content of file: include/json/reader.h
# ###################################






# ###################################
# Beginning of content of file: include/json/writer.h
# ###################################

# Copyright 2007-2010 Baptiste Lepilleur
# Distributed under MIT license, public domain if desired and
# recognized in your jurisdiction.
# See file LICENSE for detail or copy at http:#jsoncpp.sourceforge.net/LICENSE

#ifndef JSON_WRITER_H_INCLUDED
# define JSON_WRITER_H_INCLUDED

#if not defined(JSON_IS_AMALGAMATION)
# include "value.h"
#endif # if not defined(JSON_IS_AMALGAMATION)
# include <vector>
# include <string>
# include <iostream>

namespace Json
   class Value

   '''* \brief Abstract class for writers.
    '''
   class JSON_API Writer
   public:
      virtual ~Writer()

      virtual std.string write(  Value &root ) = 0


   '''* \brief Outputs a Value in <a HREF="http:#www.json.org">JSON</a> format without formatting (not human friendly).
    *
    * The JSON document is written in a single line. It is not intended for 'human' consumption,
    * but may be usefull to support feature such as RPC where bandwith is limited.
    * \sa Reader, Value
    '''
   class JSON_API FastWriter : public Writer
   public:
      FastWriter()
      virtual ~FastWriter(){

      void enableYAMLCompatibility()

   public: # overridden from Writer
      virtual std.string write(  Value &root )

   private:
      void writeValue(  Value &value )

      std.string document_
      bool yamlCompatiblityEnabled_


   '''* \brief Writes a Value in <a HREF="http:#www.json.org">JSON</a> format in a human friendly way.
    *
    * The rules for line break and indent are as follow:
    * - Object value:
    *     - if empty then print {} without indent and line break
    *     - if not empty the print '{', break & indent, one value per line
    *       and then unindent and line break and print '}'.
    * - Array value:
    *     - if empty then print [] without indent and line break
    *     - if the array contains no object value, array or some other value types,
    *       and all the values fit on one lines, print the array on a single line.
    *     - otherwise, the values do not fit on one line, the array contains
    *       object or non empty array, print one value per line.
    *
    * If the Value have comments then they are outputed according to their #CommentPlacement.
    *
    * \sa Reader, Value, Value.setComment()
    '''
   class JSON_API StyledWriter: public Writer
   public:
      StyledWriter()
      virtual ~StyledWriter(){

   public: # overridden from Writer
      '''* \brief Serialize a Value in <a HREF="http:#www.json.org">JSON</a> format.
       * \param root Value to serialize.
       * \return String containing the JSON document that represents the root value.
       '''
      virtual std.string write(  Value &root )

   private:
      void writeValue(  Value &value )
      void writeArrayValue(  Value &value )
      bool isMultineArray(  Value &value )
      void pushValue(  std.string &value )
      void writeIndent()
      void writeWithIndent(  std.string &value )
      void indent()
      void unindent()
      void writeCommentBeforeValue(  Value &root )
      void writeCommentAfterValueOnSameLine(  Value &root )
      bool hasCommentForValue(  Value &value )
      static std.string normalizeEOL(  std.string &text )

      typedef std.vector<std.string> ChildValues

      ChildValues childValues_
      std.string document_
      std.string indentString_
      int rightMargin_
      int indentSize_
      bool addChildValues_


   '''* \brief Writes a Value in <a HREF="http:#www.json.org">JSON</a> format in a human friendly way,
        to a stream rather than to a string.
    *
    * The rules for line break and indent are as follow:
    * - Object value:
    *     - if empty then print {} without indent and line break
    *     - if not empty the print '{', break & indent, one value per line
    *       and then unindent and line break and print '}'.
    * - Array value:
    *     - if empty then print [] without indent and line break
    *     - if the array contains no object value, array or some other value types,
    *       and all the values fit on one lines, print the array on a single line.
    *     - otherwise, the values do not fit on one line, the array contains
    *       object or non empty array, print one value per line.
    *
    * If the Value have comments then they are outputed according to their #CommentPlacement.
    *
    * \param indentation Each level will be indented by self amount extra.
    * \sa Reader, Value, Value.setComment()
    '''
   class JSON_API StyledStreamWriter
   public:
      StyledStreamWriter( std.string indentation="\t" )
      ~StyledStreamWriter(){

   public:
      '''* \brief Serialize a Value in <a HREF="http:#www.json.org">JSON</a> format.
       * \param out Stream to write to. (Can be ostringstream, e.g.)
       * \param root Value to serialize.
       * \note There is no point in deriving from Writer, write() should not return a value.
       '''
      void write( std.ostream &out, &root )

   private:
      void writeValue(  Value &value )
      void writeArrayValue(  Value &value )
      bool isMultineArray(  Value &value )
      void pushValue(  std.string &value )
      void writeIndent()
      void writeWithIndent(  std.string &value )
      void indent()
      void unindent()
      void writeCommentBeforeValue(  Value &root )
      void writeCommentAfterValueOnSameLine(  Value &root )
      bool hasCommentForValue(  Value &value )
      static std.string normalizeEOL(  std.string &text )

      typedef std.vector<std.string> ChildValues

      ChildValues childValues_
      std.ostream* document_
      std.string indentString_
      int rightMargin_
      std.string indentation_
      bool addChildValues_


# if defined(JSON_HAS_INT64)
   std.string JSON_API valueToString( Int value )
   std.string JSON_API valueToString( UInt value )
# endif # if defined(JSON_HAS_INT64)
   std.string JSON_API valueToString( LargestInt value )
   std.string JSON_API valueToString( LargestUInt value )
   std.string JSON_API valueToString( double value )
   std.string JSON_API valueToString( bool value )
   std.string JSON_API valueToQuotedString(  char *value )

   #/ \brief Output using the StyledStreamWriter.
   #/ \see Json.operator>>()
   std.ostream& operator<<( std.ostream&, &root )

} # namespace Json



#endif # JSON_WRITER_H_INCLUDED

# ###################################
# End of content of file: include/json/writer.h
# ###################################





#endif #ifndef JSON_AMALGATED_H_INCLUDED
